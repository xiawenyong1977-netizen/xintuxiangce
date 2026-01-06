# 扫描服务架构梳理

## 目录
1. [PC端扫描服务架构](#pc端扫描服务架构)
2. [移动端扫描服务架构](#移动端扫描服务架构)
3. [关键机制对比](#关键机制对比)

---

## PC端扫描服务架构

### 1. 扫描状态管理

#### 1.1 状态变量
- **界面层状态** (`HomeScreen.desktop.js`):
  - `isScanning`: React state，控制扫描UI状态
  - `globalMessage`: React state，显示扫描进度消息
  - `window.isScanning`: 全局变量，供其他页面检查扫描状态

- **服务层状态** (`GalleryScannerService.js`):
  - `this.isScanning`: 服务内部扫描状态标志
  - `this.isInitialized`: 服务初始化标志
  - `this.onProgress`: 进度回调函数引用

#### 1.2 状态流转
```
用户点击扫描按钮
  ↓
startSmartScan() 设置 isScanning = true, window.isScanning = true
  ↓
创建 GalleryScannerService 实例
  ↓
调用 scanGalleryWithProgress() 或 aiImageClassifyByContent()
  ↓
扫描过程中：onProgress 回调更新 globalMessage
  ↓
扫描完成：设置 isScanning = false, window.isScanning = false
```

### 2. 进度消息更新机制

#### 2.1 进度消息生成流程
```
扫描阶段执行
  ↓
sendProgressMessage(stage, processed, total, imagesClassified, totalImagesToBeClassified)
  ↓
processProgressData(rawProgress) - 生成国际化消息
  ↓
调用 onProgress 回调
  ↓
HomeScreen.handleScanProgress() 更新 globalMessage
```

#### 2.2 进度消息去重
- PC端使用 `lastProgressMessage` 键值去重
- 格式：`${stage}_${totalFoundThisPhase}_${processedThisPhase}`
- 相似度检测阶段不过滤（允许频繁更新）

#### 2.3 进度阶段定义
- `initializing`: 初始化扫描
- `directory_scanning`: 目录扫描
- `file_comparison`: 文件比对
- `screenshot_detection`: 截图检测
- `cache_checking`: 缓存检查
- `remote_inference`: 远程推理
- `local_inference`: 本地推理
- `similarity_detection`: 相似度检测
- `location_enrichment`: 位置信息补全
- `completed`: 扫描完成

### 3. 数据读写机制

#### 3.1 数据写入流程（按业务流程划分）

##### 3.1.1 基础扫描（JS层：从文件系统收集数据写入本地数据库）
```
执行层：JS层（GalleryScannerService.js）
数据来源：文件系统（文件系统遍历）
─────────────────────────────────────────────────────
1. 目录扫描
   - 使用文件系统API遍历目录
   - 收集图片文件列表（uri, fileName, size, timestamp等）
   - 不写入数据库，仅收集列表

2. 文件比对
   - 对比数据库，识别新增/删除文件
   - 删除已删除的图片（removeImagesByUris）

3. EXIF数据提取
   - 从文件系统提取EXIF数据
   - 拍摄时间（takenAt）
   - GPS坐标（latitude, longitude, altitude, accuracy）
   - 图片尺寸（width, height）
   - 拍摄参数（ISO、光圈、快门、焦距等）

4. 截图检测
   - 规则判断（文件名、尺寸、路径）
   - 分类结果：screenshot 或 NA

5. MobileNetV3推理（可选，如果设置中开启）
   - 检查 `enableMobileNetV3Classification` 设置
   - 如果开启，对每张图片进行MobileNetV3推理
   - 保存推理结果到 `mobileNetV3Detections` 字段
   - 不更新 `category` 字段（仅作为辅助信息）

6. 批量保存
   - 将图片元数据批量保存到本地数据库（IndexedDB）
   - 包括：EXIF数据、截图分类、基础信息、MobileNetV3推理结果等

后续处理（可选）：
- 基础扫描完成后，可以选择执行以下可选动作：
  - 城市信息补全（可选）
- 也可以单独触发（不依赖基础扫描完成）
```

##### 3.1.2 本地MobileNetV3推理（JS层：可选，辅助功能）
```
执行层：JS层（GalleryScannerService.js）
数据来源：文件系统（读取图片） + ONNX模型（本地推理）
触发方式：
- 在设置页面开启"使用MobileNetV3辅助分类"选项
- 基础扫描时自动执行（在基础扫描流水线的节点4）
- 位置信息补全时也会执行（如果开启选项）
─────────────────────────────────────────────────────
1. 检查设置
   - 读取 `enableMobileNetV3Classification` 设置
   - 如果开启，加载MobileNetV3模型

2. 本地MobileNetV3推理
   - 在基础扫描阶段，对每张图片进行推理
   - 使用MobileNetV3模型进行本地推理
   - 生成检测结果（mobileNetV3Detections）

3. 保存检测结果
   - 将MobileNetV3检测结果保存到本地数据库
   - 保存到 `mobileNetV3Detections` 字段
   - 不更新 `category` 字段（不作为分类依据）
   - 推理结果可在照片详情页查看

用途：
- 辅助功能：帮助用户了解图片可能的分类
- 仅供参考：准确度不高，不作为实际分类依据
- 离线可用：无需网络，完全本地推理
```

##### 3.1.3 AI分类（JS层：从后端API获取数据写入本地数据库）
```
执行层：JS层（GalleryScannerService.js）
数据来源：后端API（远程推理服务）
触发方式：用户手动触发AI分类
─────────────────────────────────────────────────────
1. 缓存检查
   - 计算图片哈希（SHA-256）
   - 查询后端API缓存（根据哈希）
   - 缓存命中：直接使用分类结果
   - 缓存未命中：继续后续流程

2. 远程推理
   - 压缩图片并上传到后端API
   - 获取AI分类结果（category, confidence, detections等）
   - 更新图片分类和置信度到本地数据库（IndexedDB）

3. 本地推理（远程服务不可用时）
   - 使用ONNX模型进行本地推理
   - 规则映射（mapDetectionsToCategory）
   - 更新图片分类和置信度到本地数据库

后续处理（可选）：
- AI分类完成后，可以选择执行后续处理（位置补全、相似度检测等）
```

##### 3.1.4 相似度检测（JS层：可选，可单独触发）
```
执行层：JS层（GalleryScannerService.js）
数据来源：文件系统（读取图片计算特征）
触发方式：
- 可选：基础扫描完成后自动执行
- 可单独触发：用户手动点击"相似度检测"按钮
─────────────────────────────────────────────────────
1. 计算图片哈希/特征
   - 从文件系统读取图片
   - 计算图片哈希（SHA-256）或特征向量

2. 检测相似图片
   - 基于哈希或特征进行相似度检测
   - 时间窗口分组（5分钟窗口）
   - 相似度阈值判断（0.8）

3. 写入相似组数据
   - 将相似组信息写入本地数据库
   - 更新图片的相似组关联（similarity_group_id等）
```

##### 3.1.5 城市信息补全（JS层：可选，可单独触发）
```
执行层：JS层（GalleryScannerService.js）
数据来源：后端API（位置查询服务）或本地位置数据库（Location.db）
触发方式：
- 可选：基础扫描完成后自动执行
- 可单独触发：用户手动点击"位置信息补全"按钮
─────────────────────────────────────────────────────
1. 查询需要补全的图片
   - 从数据库读取有GPS坐标但没有位置信息的图片
   - 排除截图和二维码分类的图片

2. 查询城市信息
   - 根据GPS坐标批量查询后端API（v2批量接口）
   - 或查询本地位置数据库（Location.db）
   - 获取城市信息（name_en, name_zh, province, country_code等）

3. 保存位置详情
   - 将位置信息保存到本地位置数据库（Location.db）
   - 生成location_id并保存位置详情

4. 更新图片位置信息
   - 更新图片的位置信息到本地数据库
   - 包括：city（存储location_id）、province、country等

性能优化：流水线并行处理架构
─────────────────────────────────────────────────────
核心难点：处理大量照片时，需要平衡CPU密集型任务（MobileNetV3推理）和
         IO密集型任务（位置查询、数据库写入），避免阻塞UI线程。

流水线架构（Pipeline Architecture）：
┌─────────────────────────────────────────────────────────────┐
│  批次输入（每批50张图片）                                    │
└─────────────────────────────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────────┐
    │  节点1：MobileNetV3推理（单线程）      │
    │  - 从队列取批次任务                    │
    │  - 并行推理批次内所有图片              │
    │  - 每5个批次批量保存推理结果           │
    │  - 将结果传递给节点2                   │
    └───────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────────┐
    │  节点2：位置查询（单线程）             │
    │  - 累积坐标到400个后批量查询           │
    │  - 调用后端API批量查询位置信息         │
    │  - 批量保存位置详情和图片位置信息      │
    └───────────────────────────────────────┘

性能优化策略：
1. 批次处理
   - 每批处理50张图片，避免内存占用过大
   - 批次间异步处理，不阻塞UI线程

2. 流水线并行
   - 节点1（推理）和节点2（位置查询）并行运行
   - 推理完成后立即传递给位置查询，无需等待
   - 充分利用CPU和网络IO的并行性

3. 批量操作优化
   - MobileNetV3推理结果：每5个批次（250张）批量保存一次
   - 位置查询：累积到400个坐标后批量查询（API限制500个）
   - 减少数据库写入次数，提升整体性能

4. 异步非阻塞
   - 使用Promise.all并行处理批次内图片
   - 节点间通过队列传递数据，避免同步等待
   - 定期让出控制权（setTimeout），避免阻塞UI线程

5. 进度更新策略
   - 位置信息补全：每处理50张图片触发一次刷新
   - 避免频繁刷新导致UI卡顿
```



#### 3.2 数据缓存与界面数据交换机制

##### 3.2.1 缓存优先读取机制
```
核心原则：界面始终从缓存读取数据，避免异步延迟，提升响应速度

数据流向：
数据库（SQLite/IndexedDB）
    ↓
ImageStorageService.getImages()（转换为精简结构）
    ↓
GlobalImageCache.buildCache()（构建内存缓存）
    ↓
UnifiedDataService.readAllImages()（从缓存读取）
    ↓
界面组件（HomeScreen, CategoryScreen等）

关键特性：
- 缓存是单例模式（GlobalImageCache），避免重复加载
- 界面读取数据时，优先从缓存读取，无需等待数据库查询
- 缓存更新后，通过监听器机制通知界面刷新
- 避免异步操作带来的响应延迟，提升用户体验
```

##### 3.2.2 数据分级策略（精简信息 vs 详细信息）
```
核心目标：优化内存占用，只缓存界面必需的数据

精简信息（存储在缓存中）：
─────────────────────────────────────────────────────
包含字段：
- 基础信息：id, uri, fileName, timestamp, takenAt
- 分类信息：category, city, country
- 显示信息：size, mimeType, background_color
- 尺寸信息：width, height（从imageDimensions提取）
- GPS坐标：latitude, longitude（用于位置信息补全）
- 拍摄参数分类：isoCategory, apertureCategory, shutterCategory, focalLengthCategory
- 拍摄参数：cameraSettings（JSON对象）

不包含字段（按需从数据库加载）：
- 推理结果：generalDetections, idCardDetections, mobileNetV3Detections
- 大模型描述：message
- 相似度信息：similarity_group_id, similarity_group_type
- 其他详细字段：address, province, district, street等

详细信息（存储在数据库中，按需加载）：
─────────────────────────────────────────────────────
- 完整的数据库记录，包含所有字段
- 通过 getImagesByIds() 批量加载
- 仅在需要时加载（如相似度检测、图片详情页）

内存优化效果：
- 假设有10000张图片，每张图片精简信息约500字节
- 缓存总大小：10000 × 500字节 ≈ 5MB
- 如果包含推理结果，每张图片约5KB
- 完整缓存大小：10000 × 5KB ≈ 50MB
- 内存节省：约90%
```

##### 3.2.3 按需加载详细信息
```
使用场景：相似度检测、图片详情页等需要推理结果的场景

加载流程：
1. 从缓存读取精简信息（快速，无延迟）
   const images = await UnifiedDataService.readAllImages();
   
2. 按需批量加载详细信息
   const imageIds = images.map(img => img.id);
   const detailedMap = await storageService.getImagesByIds(imageIds);
   
3. 合并数据
   const enhancedImages = images.map(img => ({
     ...img, // 精简信息
     ...detailedMap.get(img.id) // 详细信息
   }));

优势：
- 界面快速响应：先显示精简信息，再异步加载详细信息
- 内存占用可控：只加载当前需要的详细信息
- 批量加载优化：一次性加载多个图片的详细信息，减少数据库查询次数
```

##### 3.2.5 多维度分类支持机制
```
核心设计：通过精简信息中的分类字段 + 缓存中的统计对象，支持多维度分类

当前支持的分类维度（11个）：
─────────────────────────────────────────────────────
1. AI分类（categoryCounts）
   - 字段：category
   - 统计：按AI分类结果统计（single_person, pets, foods等）

2. 城市分类（cityCounts）
   - 字段：city（存储location_id）
   - 统计：按城市统计

3. 颜色分类（colorCounts）
   - 字段：background_color
   - 统计：按背景颜色统计

4. 目录分类（directoryCounts）
   - 字段：uri（提取目录路径）
   - 统计：按存储目录统计

5. 格式分类（formatCounts）
   - 字段：mimeType
   - 统计：按图片格式统计（image/jpeg, image/png等）

6. 分辨率分类（resolutionCounts）
   - 字段：width, height（从imageDimensions提取）
   - 统计：按分辨率分类统计（1080p, 4K等）

7. 方向分类（orientationCounts）
   - 字段：width, height
   - 统计：按方向统计（横屏、竖屏、全景）

8. ISO分类（isoCounts）
   - 字段：isoCategory（从cameraSettings计算）
   - 统计：按ISO值分类统计

9. 光圈分类（apertureCounts）
   - 字段：apertureCategory（从cameraSettings计算）
   - 统计：按光圈值分类统计

10. 快门分类（shutterCounts）
    - 字段：shutterCategory（从cameraSettings计算）
    - 统计：按快门速度分类统计

11. 焦距分类（focalLengthCounts）
    - 字段：focalLengthCategory（从cameraSettings计算）
    - 统计：按焦距值分类统计

实现机制：
─────────────────────────────────────────────────────
1. 精简信息中包含分类字段
   - 每个维度对应一个字段（如isoCategory, apertureCategory等）
   - 字段值在扫描时计算并存储到数据库
   - 构建缓存时直接读取，无需重新计算

2. 缓存中维护统计对象
   - 每个维度对应一个统计对象（如isoCounts, apertureCounts等）
   - 统计对象格式：{ "分类值": 数量, ... }
   - 例如：{ "low": 100, "medium": 200, "high": 50 }

3. 统计重建机制
   - buildCache()：遍历所有图片，重建所有维度统计
   - addImageToCache()：增量更新所有维度统计
   - updateImageClassification()：重建所有维度统计（批量更新时优化）

增加一个维度的开销分析：
─────────────────────────────────────────────────────
假设有10000张图片，增加一个新维度（如"设备分类"）：

1. 内存开销
   ─────────────────────────────────────────────────
   精简信息字段：
   - 每张图片增加1个字段（如deviceCategory: "iPhone"）
   - 字段大小：约20字节（字符串）
   - 总开销：10000 × 20字节 = 200KB
   
   统计对象：
   - 统计对象大小：约1-5KB（取决于分类值数量）
   - 例如：{ "iPhone": 3000, "Android": 5000, "Camera": 2000 }
   - 总开销：约5KB
   
   合计：约205KB（可忽略不计）

2. 性能开销
   ─────────────────────────────────────────────────
   构建缓存时（buildCache）：
   - 需要遍历所有图片计算统计：O(n)
   - 每张图片处理时间：约0.001ms（字段读取 + 统计累加）
   - 总时间：10000 × 0.001ms = 10ms
   - 影响：可忽略不计（构建缓存总时间约100-500ms）
   
   增量添加时（addImageToCache）：
   - 单张图片统计更新：O(1)
   - 处理时间：约0.001ms
   - 影响：可忽略不计
   
   批量更新时（updateImageClassification）：
   - 重建统计：O(n)
   - 处理时间：约10ms（与构建缓存相同）
   - 影响：可忽略不计（批量更新总时间约50-200ms）

3. 数据库开销
   ─────────────────────────────────────────────────
   存储字段：
   - 数据库增加1个字段（如device_category TEXT）
   - 每张图片增加约20字节存储
   - 总开销：10000 × 20字节 = 200KB
   - 影响：可忽略不计（数据库总大小约50-100MB）

4. 代码维护开销
   ─────────────────────────────────────────────────
   需要添加的代码：
   - 精简信息字段提取：约5行
   - 统计重建函数：约10行
   - 增量更新逻辑：约5行
   - 界面显示逻辑：约20-50行
   - 合计：约40-70行代码

总结：
─────────────────────────────────────────────────────
- 内存开销：约205KB（可忽略不计）
- 性能开销：构建缓存增加约10ms（可忽略不计）
- 数据库开销：约200KB（可忽略不计）
- 代码维护：约40-70行代码（中等开销）

结论：增加一个维度的开销非常小，系统设计支持轻松扩展新维度
```

##### 3.2.4 统一数据服务接口
```
UnifiedDataService（统一数据服务）
─────────────────────────────────────────────────────
读接口（优先从缓存读取）：
- readAllImages(): 读取所有图片（精简信息）
- readCategoryCounts(): 读取分类统计
- readCityCounts(): 读取城市统计
- readSimilarityGroupsStats(): 读取相似组统计
- getImageById(id): 根据ID获取图片（优先缓存，无则数据库）

写接口（更新数据库后刷新缓存）：
- writeImageDetailedInfo(): 写入图片详细信息
- batchUpdateClassification(): 批量更新分类
- updateImagesCity(): 批量更新位置信息
- removeImagesByUris(): 删除图片

缓存管理：
- buildCache(): 构建/重建缓存
- getCache(): 获取缓存对象（同步，无延迟）

监听器机制说明：
- notifyListeners(): 通知监听器缓存已更新
- addListener(): 添加缓存变化监听器
- 当前状态：监听器机制已实现，但界面未使用
- 界面刷新方式：采用主动拉取模式
  - 通过 `loadData()` / `loadAllData()` 主动刷新数据
  - 在扫描完成、位置补全等关键节点触发刷新
  - 使用 `useFocusEffect` 在页面聚焦时刷新
- 监听器用途：为未来扩展预留，可用于实现响应式数据更新
```

#### 3.3 数据刷新策略
- **扫描完成时**: `progress.shouldRefresh === true` 时刷新
- **位置信息补全**: 每处理50张图片触发一次刷新
- **相似度检测**: 每检测完一个相似组触发刷新
- **防抖机制**: PC端无防抖，直接刷新

### 4. 界面数据刷新

#### 4.1 刷新触发点
```javascript
// HomeScreen.desktop.js
handleScanProgress(progress) {
  // 扫描完成时刷新
  if (progress.stage === 'completed' && progress.shouldRefresh) {
    loadData();
  }
  
  // 位置信息补全阶段刷新
  if (progress.stage === 'location_enrichment' && progress.shouldRefresh) {
    setTimeout(() => loadData(), 0);
  }
}
```

#### 4.2 刷新内容
- 分类统计 (`loadCategories()`)
- 城市统计 (`loadCities()`)
- 相似组统计 (`loadSimilarityGroups()`)
- 最近照片 (`loadRecentImages()`)
- 其他分类数据（颜色、目录、格式等）

---

## 移动端扫描服务架构

### 1. 扫描状态管理

#### 1.1 状态变量
- **界面层状态** (`HomeScreen.mobile.js`):
  - `isScanning`: React state，控制扫描UI状态
  - `globalMessage`: React state，显示扫描进度消息
  - `window.isScanning`: 全局变量，供其他页面检查扫描状态

- **JS服务层状态** (`GalleryScannerService.android.js`):
  - `this.isScanning`: JS层扫描状态标志
  - `this.currentScanId`: 当前扫描任务ID
  - `this.onProgress`: 进度回调函数引用
  - `this.eventEmitter`: 原生事件监听器

- **原生层状态** (`GalleryScanService.java`):
  - 扫描任务状态（运行中/已完成/已取消）
  - 扫描进度统计（已处理/总数）

#### 1.2 状态流转
```
用户点击扫描按钮
  ↓
executeAIClassify() 设置 isScanning = true, window.isScanning = true
  ↓
创建 GalleryScannerService 实例
  ↓
调用 aiImageClassifyByContent()
  ↓
JS层调用原生层 startScan()
  ↓
原生层启动扫描任务（后台线程）
  ↓
原生层发送进度事件到JS层
  ↓
JS层 processProgressData() 处理进度
  ↓
调用 onProgress 回调更新UI
  ↓
扫描完成：原生层发送完成事件
  ↓
JS层执行后续处理（位置补全、相似度检测）
  ↓
设置 isScanning = false, window.isScanning = false
```

### 2. 进度消息更新机制

#### 2.1 进度消息生成流程（三层架构）
```
原生层扫描线程
  ↓
sendProgressEvent(stage, filesProcessed, filesFound, ...)
  ↓
发送 "GalleryScanProgress" 事件到JS层
  ↓
JS层监听事件 → handleProgressEvent()
  ↓
processProgressData() 生成国际化消息
  ↓
sendProgressMessage() 处理进度更新
  ├─ 更新前台服务通知（ScanService.updateProgress）
  │  - 只有原生扫描流程使用前台服务
  │  - 相似度检测和位置信息补全不使用（JS线程运行）
  └─ 调用 onProgress 回调更新UI
  ↓
HomeScreen.handleScanProgress() 更新 globalMessage
```

#### 2.2 前台服务通知更新
- **服务启动**: `ScanService.startScanService()` 启动前台服务
- **进度更新**: `ScanService.updateProgress(message, processed, total, title)`
- **服务停止**: `ScanService.stopScanService()` 停止前台服务
- **心跳机制**: 每10秒更新一次通知，保持服务活跃

#### 2.3 进度消息去重
- 移动端**不移除去重逻辑**，允许所有进度更新通过
- 原因：原生层已经控制更新频率，JS层不需要再次过滤

### 3. 数据读写机制

#### 3.1 原生层数据写入

##### 3.1.1 基础扫描流程（独立流程）
```
原生层扫描线程
  ↓
MediaStore扫描 → 读取图片元数据
  ↓
文件比对 → 检查数据库是否存在
  ↓
EXIF提取 → 提取GPS、拍摄参数等
  ↓
截图检测 → 规则分类（screenshot）
  ↓
批量写入数据库（SQLite）
  ↓
发送进度事件到JS层（basic_scan_completed）
  ↓
JS层可选执行后续处理（位置补全、相似度检测）
```

##### 3.1.2 AI分类流程（独立流程，用户手动触发）
```
用户手动触发AI分类
  ↓
原生层AI分类线程
  ↓
缓存检查 → 查询后端API缓存
  ├─ 缓存命中：直接保存分类结果
  └─ 缓存未命中：继续后续流程
  ↓
远程推理 → 调用后端API分类
  ↓
批量写入数据库（SQLite）
  ↓
发送进度事件到JS层（ai_classification_completed）
```

#### 3.2 JS层数据读取
- 与PC端相同，使用 `UnifiedDataService` 统一接口
- 支持缓存机制，减少数据库查询

#### 3.3 数据刷新策略
- **防抖机制**: 使用 `loadAllDataDebounced()` 防抖刷新（500ms）
- **刷新触发**:
  - 扫描完成时：清除防抖定时器，延迟600ms后刷新
  - 位置信息补全：每处理50张图片触发防抖刷新
  - 相似度检测：每检测完一个相似组触发防抖刷新

### 4. 界面数据刷新

#### 4.1 刷新触发点
```javascript
// HomeScreen.mobile.js
galleryScannerService.onProgress = (progress) => {
  // 更新消息
  setGlobalMessage(progress.simpleMessage || progress.message);
  
  // 防抖刷新
  if (progress.shouldRefresh) {
    loadAllDataDebounced();
  }
};

// 扫描完成后
if (loadDataDebounceTimerRef.current) {
  clearTimeout(loadDataDebounceTimerRef.current);
}
await new Promise(resolve => setTimeout(resolve, 600));
await loadAllData();
```

#### 4.2 防抖机制
```javascript
const loadAllDataDebounced = useCallback(() => {
  if (loadDataDebounceTimerRef.current) {
    clearTimeout(loadDataDebounceTimerRef.current);
  }
  loadDataDebounceTimerRef.current = setTimeout(async () => {
    await loadAllData();
  }, 500);
}, [loadAllData]);
```


### 6. 移动层架构（三层）

#### 6.1 前台服务层 (`ScanForegroundService.java`)
- **职责**: 保持应用在后台运行时继续扫描
- **机制**:
  - 前台通知显示扫描进度
  - WakeLock防止CPU休眠
  - 心跳机制（10秒）保持服务活跃
- **生命周期**:
  - `START_SCAN`: 启动服务，获取WakeLock
  - `UPDATE_PROGRESS`: 更新通知内容
  - `STOP_SCAN`: 停止服务，释放WakeLock

#### 6.2 原生层 (`GalleryScanService.java`)
- **职责**: 执行实际的扫描和分类任务
- **机制**:
  - 独立后台线程执行扫描
  - MediaStore API扫描图片
  - SQLite数据库批量写入
  - MobileNetV3模型推理
- **事件通信**:
  - `GalleryScanProgress`: 进度事件
  - `GalleryScanCompleted`: 完成事件
  - `GalleryScanError`: 错误事件

#### 6.3 JS层 (`GalleryScannerService.android.js`)
- **职责**: 协调原生层和界面层
- **机制**:
  - 监听原生层事件
  - 处理进度数据国际化
  - 更新前台服务通知
  - 执行JS层后续处理（位置补全、相似度检测）
- **桥接模块** (`ScanServiceModule.java`):
  - `startScanService()`: 启动前台服务
  - `updateScanProgress()`: 更新进度通知
  - `stopScanService()`: 停止前台服务

---

## 关键机制对比

### 1. 扫描状态管理

| 特性 | PC端 | 移动端 |
|------|------|--------|
| 状态变量 | `isScanning`, `window.isScanning` | `isScanning`, `window.isScanning` |
| 状态设置时机 | 扫描开始时 | 扫描开始时 |
| 状态清除时机 | 扫描完成/失败时 | 扫描完成/失败时 |
| 全局状态 | `window.isScanning` | `window.isScanning` |

### 2. 进度消息更新

| 特性 | PC端 | 移动端 |
|------|------|--------|
| 消息生成 | JS层 `processProgressData()` | JS层 `processProgressData()` |
| 消息去重 | 有（基于消息键值） | 无（原生层已控制频率） |
| 通知更新 | 无（PC端不需要） | 有（前台服务通知） |
| 更新频率 | 每个阶段更新 | 原生层控制频率 |

### 3. 数据读写

| 特性 | PC端 | 移动端 |
|------|------|--------|
| 扫描实现 | JS层实现 | 原生层实现 |
| 数据库操作 | JS层直接操作 | 原生层批量操作 |
| 数据刷新 | 直接刷新 | 防抖刷新（500ms） |
| 刷新触发 | `shouldRefresh` 标志 | `shouldRefresh` 标志 |

### 4. 界面刷新

| 特性 | PC端 | 移动端 |
|------|------|--------|
| 刷新方式 | 直接调用 `loadData()` | 防抖调用 `loadAllDataDebounced()` |
| 刷新时机 | 扫描完成、位置补全 | 扫描完成、位置补全、相似度检测 |
| 防抖机制 | 无 | 有（500ms延迟） |

### 5. 新增分类处理

| 特性 | PC端 | 移动端 |
|------|------|--------|
| AI分类实现 | JS层MobileNetV3 | 原生层MobileNetV3 |
| 批量处理 | JS层批次处理 | 原生层批次处理 |
| 后续处理 | 位置补全、相似度检测 | 位置补全、相似度检测 |
| 数据更新 | 直接更新数据库 | 原生层批量更新数据库 |

### 6. 后台执行能力

| 特性 | PC端 | 移动端 |
|------|------|--------|
| 后台扫描 | 支持（Electron主进程） | 支持（前台服务） |
| 进程保活 | 不需要 | WakeLock + 前台服务 |
| 通知显示 | 不需要 | 前台服务通知 |
| 心跳机制 | 不需要 | 10秒心跳更新通知 |

---

## 总结

### PC端特点
1. **纯JS实现**: 所有扫描逻辑在JS层实现
2. **简单直接**: 状态管理和进度更新简单直接
3. **无后台限制**: Electron主进程可以长时间运行
4. **无防抖**: 数据刷新直接执行，无需防抖

### 移动端特点
1. **三层架构**: 前台服务 + 原生层 + JS层
2. **后台保活**: 前台服务 + WakeLock确保后台执行
3. **防抖刷新**: 避免频繁刷新影响性能
4. **原生性能**: 原生层扫描和AI分类性能更好

### 共同点
1. **统一接口**: 都使用 `GalleryScannerService` 统一接口
2. **进度回调**: 都使用 `onProgress` 回调更新UI
3. **数据服务**: 都使用 `UnifiedDataService` 统一数据接口
4. **状态管理**: 都使用 `isScanning` 和 `window.isScanning` 管理状态

