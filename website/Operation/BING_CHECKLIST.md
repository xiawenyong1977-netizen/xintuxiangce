# Bing Webmaster Tools 检查清单

生成时间: 2026-01-18 09:27:30


请在 Bing Webmaster Tools 中执行以下检查：

【检查 1: site: 搜索结果】❌ 当前状态：返回结果为空
1. 在 Bing 搜索框中输入: site:www.xintuxiangce.top
2. 查看返回的搜索结果数量
   ✅ 如果返回很多结果 → 索引正常
   ❌ 如果返回很少或为空 → 索引问题（当前状态）
   
⚠️ **紧急**: site: 搜索为空说明页面完全没有被索引！
   请立即执行 Operation/BING_INDEX_EMPTY_SOLUTION.md 中的解决方案

【检查 2: 索引覆盖报告】
1. 登录 Bing Webmaster Tools: https://www.bing.com/webmasters
2. 找到索引相关信息的正确位置（根据界面版本可能不同）:
   
   方法 A（新版界面）:
   - 左侧菜单 → "索引" 或 "Indexing"
   - 查看 "已索引页面" 或 "Indexed Pages" 数量
   - 查看 "排除的页面" 或 "Excluded Pages"
   
   方法 B（旧版界面）:
   - 左侧菜单 → "网站诊断" → "索引"
   - 或 "诊断和工具" → "索引管理器"
   
   方法 C（如果找不到）:
   - 左侧菜单 → "报告" → "索引统计"
   - 或直接查看首页的 "索引页面数" 卡片
   
3. 需要查看的关键指标:
   - ✅ 已索引页面数量（应该是 > 0）
   - ❌ "Excluded by policy"（政策排除）
   - ❌ "Low quality content"（低质量内容）
   - ⚠️ "Discovered but not crawled"（已发现但未抓取）
   - ❌ "Crawl errors"（抓取错误）

【检查 3: URL 检查工具】
1. 在 Bing Webmaster Tools 中使用 "URL 检查工具"
2. 测试以下页面:
   - https://www.xintuxiangce.top/
   - https://www.xintuxiangce.top/guides.html
   - https://www.xintuxiangce.top/faq.html
3. 确认每个页面:
   ✅ 页面可以抓取
   ✅ 页面可以索引
   ✅ 没有被 robots 或 meta 阻止

【检查 4: 站点地图状态】
1. 导航到: 站点地图
2. 检查 sitemap.xml 的状态:
   ✅ 已提交
   ✅ 状态正常
   ✅ 最近有更新

【检查 5: 抓取统计】
1. 导航到: 抓取统计
2. 查看 bingbot 的抓取情况:
   ✅ 最近有抓取活动
   ✅ 没有大量错误

【检查 6: 安全与手动操作】
1. 导航到: 安全与手动操作
2. 检查是否有:
   ❌ 手动操作（Manual Actions）
   ❌ 安全问题（Security Issues）
