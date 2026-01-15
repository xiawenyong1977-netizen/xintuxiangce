
import React, { useEffect, useState } from 'react';
import { 
  ShieldCheck, 
  Zap, 
  LayoutGrid, 
  Smartphone, 
  Monitor, 
  CheckCircle2, 
  ChevronRight,
  Clock,
  MapPin,
  Palette,
  Maximize,
  HardDrive,
  FileCode,
  RotateCcw,
  Aperture,
  Cpu,
  Camera,
  Search,
  Sparkles,
  Focus,
  XCircle,
  Settings2,
  Filter,
  Check,
  Download
} from 'lucide-react';

// 平台检测工具函数
const detectPlatform = (): 'android' | 'windows' | 'ios' | 'mac' | 'linux' | 'unknown' => {
  if (typeof window === 'undefined') return 'unknown';
  
  const userAgent = navigator.userAgent || navigator.vendor || (window as any).opera;
  
  // 检测 Android
  if (/android/i.test(userAgent)) {
    return 'android';
  }
  
  // 检测 iOS/Mac
  if (/iPad|iPhone|iPod/.test(userAgent) && !(window as any).MSStream) {
    return 'ios';
  }
  if (/Macintosh|Mac OS X/.test(userAgent)) {
    return 'mac';
  }
  
  // 检测 Windows
  if (/Windows/i.test(userAgent)) {
    return 'windows';
  }
  
  // 检测 Linux
  if (/Linux/.test(userAgent)) {
    return 'linux';
  }
  
  return 'unknown';
};

// 根据平台获取推荐下载链接
const getRecommendedDownloadLink = (platform: string): string => {
  switch (platform) {
    case 'android':
      return '/download.py?type=android';
    case 'windows':
    case 'linux':
      return '/download.py?type=setup';
    case 'mac':
      return '/download.py?type=setup'; // Mac 暂时使用 setup，后续可以添加 Mac 版本
    default:
      return '/download.py?type=setup'; // 默认使用 setup
  }
};

// --- Components ---

// Navbar 和 Footer 已移除，使用公共组件（通过 components-loader.js 加载）

const Hero: React.FC = () => {
  const [platform, setPlatform] = useState<string>('unknown');
  
  useEffect(() => {
    setPlatform(detectPlatform());
  }, []);
  
  const recommendedLink = getRecommendedDownloadLink(platform);
  
  return (
    <section className="pt-20 pb-20 px-6 relative overflow-hidden">
      <div className="absolute -top-20 -right-20 w-96 h-96 bg-emerald-50 rounded-full blur-3xl opacity-60"></div>
      <div className="absolute top-40 -left-20 w-72 h-72 bg-teal-50 rounded-full blur-3xl opacity-60"></div>
      
      <div className="max-w-7xl mx-auto text-center relative z-10">
        <div className="inline-flex items-center space-x-2 bg-emerald-50 text-emerald-700 px-4 py-1.5 rounded-full text-sm font-medium mb-6 border border-emerald-100">
          <Check className="w-4 h-4" />
          <span>本地智能整理 · 还原纯净相册</span>
        </div>
        <h1 className="text-5xl md:text-7xl font-bold mb-8 tracking-tight text-slate-900 leading-tight">
          让相册回归有序<br/><span className="bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-600">让每一刻都有迹可循</span>
        </h1>
        <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto mb-10 leading-relaxed">
          芯图是一款简单且纯净的本地管理工具。它能自动将海量照片按时间、内容、色彩等12个维度分门别类，并精准排除广告和垃圾图的干扰。
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <a 
            href={recommendedLink}
            className="w-full sm:w-auto px-8 py-4 bg-emerald-600 text-white rounded-2xl font-bold hover:bg-emerald-700 transition-all flex items-center justify-center shadow-lg shadow-emerald-200 active:scale-95"
          >
            极速整理相册 <ChevronRight className="ml-2 w-5 h-5" />
          </a>
          <a 
            href="https://xiawenyong1977-netizen.github.io/xintu-privacy-policy/"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full sm:w-auto px-8 py-4 bg-white text-slate-900 border border-slate-200 rounded-2xl font-bold hover:bg-slate-50 transition-all active:scale-95"
          >
            查看隐私承诺
          </a>
        </div>

        <div className="mt-20 relative max-w-5xl mx-auto">
          <div className="aspect-[16/9] bg-slate-200 rounded-3xl shadow-2xl overflow-hidden border-8 border-white animate-float">
             <img src="https://images.unsplash.com/photo-1554080353-a576cf803bda?auto=format&fit=crop&q=80&w=1600" alt="Xintu Interface" className="w-full h-full object-cover" />
             <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/10 backdrop-blur-[1px]">
                <div className="bg-white/95 p-6 rounded-2xl shadow-2xl flex items-center space-x-4">
                    <LayoutGrid className="text-emerald-600 w-8 h-8" />
                    <div className="text-left">
                        <div className="text-slate-900 font-bold">已为您自动分类</div>
                        <div className="text-emerald-600 text-sm font-medium">12个维度 · 纯净空间</div>
                    </div>
                </div>
             </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const FeatureCard: React.FC<{ icon: React.ReactNode, title: string, desc: string, color: string, badge?: string }> = ({ icon, title, desc, color, badge }) => (
  <div className="group relative p-1 rounded-[2rem] overflow-hidden transition-all duration-500">
    <div className="relative h-full bg-white rounded-[1.9rem] p-8 flex flex-col items-start shadow-sm border border-slate-100 hover:shadow-xl transition-all duration-500 hover:border-emerald-100">
      <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 transition-all duration-500 group-hover:scale-110 shadow-inner ${color}`}>
        <div className="text-slate-800 transition-colors group-hover:text-emerald-700">
          {icon}
        </div>
      </div>
      
      <div className="flex items-center justify-between w-full mb-3">
        <h3 className="text-xl font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">{title}</h3>
      </div>
      
      <p className="text-slate-500 text-sm leading-relaxed mb-6">
        {desc}
      </p>

      <div className="absolute -bottom-6 -right-6 text-slate-50 opacity-0 group-hover:opacity-10 pointer-events-none transition-opacity">
        {React.isValidElement(icon) ? React.cloneElement(icon as React.ReactElement<any>, { size: 100 }) : icon}
      </div>
    </div>
  </div>
);

const Features: React.FC = () => {
  return (
    <section id="features" className="py-32 bg-slate-50 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-20 gap-8">
          <div className="max-w-xl">
            <h2 className="text-sm font-bold text-emerald-600 uppercase tracking-[0.2em] mb-4">Core Values</h2>
            <h3 className="text-4xl md:text-5xl font-black text-slate-900 leading-[1.1]">
              管理变简单<br/>让照片<span className="text-emerald-600">各就其位</span>
            </h3>
          </div>
          <p className="text-slate-500 max-w-sm border-l-2 border-emerald-200 pl-6 py-2">
            我们致力于提供一种简单、安全、不打扰的管理方案，让每个人都能轻松享受整理照片的乐趣。
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard 
            icon={<ShieldCheck className="w-7 h-7" />}
            title="本地处理最放心"
            desc="所有照片都在设备本地扫描，数据永不离端，不联网也可用。保护隐私是我们的第一准则。"
            color="bg-emerald-50"
            badge="Privacy"
          />
          <FeatureCard 
            icon={<LayoutGrid className="w-7 h-7" />}
            title="12维智能分类"
            desc="独有的12个分类维度，无论是按拍摄参数还是按内容语义，都能实现自动化归位，找图只需一瞬。"
            color="bg-emerald-50"
            badge="Intelligent"
          />
          <FeatureCard 
            icon={<Filter className="w-7 h-7" />}
            title="远离杂讯干扰"
            desc="精准识别非摄影类图片，智能屏蔽应用广告与缓存缩略图。不修改源文件，仅展示您关心的内容。"
            color="bg-teal-50"
            badge="Clean"
          />
          <FeatureCard 
            icon={<Settings2 className="w-7 h-7" />}
            title="灵活自主管理"
            desc="自由指定需要扫描的目录，完全遵循您的文件管理逻辑。不多扫、不乱扫，让管理更从容。"
            color="bg-emerald-50"
            badge="Control"
          />
        </div>
      </div>
    </section>
  );
};

const DimensionCard: React.FC<{ icon: React.ReactNode, label: string, color: string, ai?: boolean }> = ({ icon, label, color, ai }) => (
  <div className="dimension-card group relative p-6 bg-white rounded-2xl shadow-lg border border-slate-100 flex flex-col items-center justify-center text-center hover:z-20 hover:shadow-2xl hover:shadow-emerald-500/20">
    <div className={`w-12 h-12 mb-4 rounded-xl flex items-center justify-center transition-all duration-500 group-hover:scale-125 group-hover:bg-opacity-100 ${color} bg-opacity-10`}>
      <div className="text-slate-800 transition-colors group-hover:text-white">
        {icon}
      </div>
    </div>
    <span className="text-sm font-bold text-slate-700 tracking-wide group-hover:text-emerald-600">{label}</span>
    {ai && (
      <div className="absolute top-2 right-2">
        <Sparkles className="w-3 h-3 text-emerald-500 opacity-60" />
      </div>
    )}
  </div>
);

const Dimensions: React.FC = () => {
  const list = [
    { icon: <Clock />, label: "时光轴", color: "bg-emerald-500 text-emerald-500" },
    { icon: <Camera />, label: "场景识别", color: "bg-teal-500 text-teal-500", ai: true },
    { icon: <MapPin />, label: "足迹地图", color: "bg-emerald-500 text-emerald-500" },
    { icon: <Palette />, label: "色彩心情", color: "bg-lime-500 text-lime-500", ai: true },
    { icon: <Maximize />, label: "清晰度", color: "bg-emerald-500 text-emerald-500" },
    { icon: <HardDrive />, label: "存储占用", color: "bg-emerald-500 text-emerald-500" },
    { icon: <FileCode />, label: "格式类型", color: "bg-emerald-500 text-emerald-500" },
    { icon: <RotateCcw />, label: "画面方向", color: "bg-emerald-500 text-emerald-500" },
    { icon: <Aperture />, label: "大片感", color: "bg-emerald-500 text-emerald-500" },
    { icon: <Cpu />, label: "拍摄质量", color: "bg-emerald-500 text-emerald-500" },
    { icon: <Zap />, label: "动作抓拍", color: "bg-emerald-500 text-emerald-500" },
    { icon: <Focus />, label: "远近特写", color: "bg-emerald-500 text-emerald-500" }
  ];

  return (
    <section id="dimensions" className="py-24 bg-slate-900 overflow-hidden relative">
      <div className="absolute inset-0 overflow-hidden opacity-30">
        <div className="scan-line"></div>
      </div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="text-center mb-20">
          <h2 className="text-4xl md:text-6xl font-black text-white mb-6">
            12个维度的<span className="text-emerald-500">智能分类</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            系统自动为您打好标签。无论是按拍摄日期、地点，还是寻找照片中的蓝天、草原，一切都井井有条。
          </p>
        </div>
        
        <div className="perspective-grid grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          {list.map((item, idx) => (
            <DimensionCard key={idx} icon={item.icon} label={item.label} color={item.color} ai={item.ai} />
          ))}
        </div>
      </div>
    </section>
  );
};

const ComparisonRow: React.FC<{ 
  title: string, 
  systemText: string, 
  xintuText: string, 
  icon: React.ReactNode
}> = ({ title, systemText, xintuText, icon }) => (
  <div className="grid grid-cols-1 md:grid-cols-[1.2fr_2fr_2fr] gap-4 md:gap-0 border-b border-slate-100 last:border-0 hover:bg-slate-50/50 transition-colors">
    <div className="py-6 px-4 md:px-8 flex items-center space-x-3 md:bg-white/50">
      <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500">
        {icon}
      </div>
      <span className="font-bold text-slate-900">{title}</span>
    </div>
    
    <div className="py-6 px-4 md:px-12 flex items-start space-x-3 bg-white/30">
      <XCircle className="w-5 h-5 text-slate-300 mt-1 flex-shrink-0" />
      <span className="text-slate-500 text-sm leading-relaxed">{systemText}</span>
    </div>
    
    <div className="py-6 px-4 md:px-12 flex items-start space-x-3 bg-emerald-50/50">
      <CheckCircle2 className="w-5 h-5 text-emerald-600 mt-1 flex-shrink-0" />
      <span className="text-slate-900 text-sm font-medium leading-relaxed">{xintuText}</span>
    </div>
  </div>
);

const Comparison: React.FC = () => {
  return (
    <section id="comparison" className="py-32 bg-white overflow-hidden">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-20">
          <h2 className="text-3xl md:text-5xl font-black mb-6">
            为何选择 <span className="text-emerald-600">芯图相册？</span>
          </h2>
          <p className="text-slate-500 text-lg">回归管理本质：让相册服务于影像，提供更纯净的视觉享受。</p>
        </div>

        <div className="rounded-[2.5rem] border border-slate-100 shadow-2xl overflow-hidden bg-slate-50/20">
          <div className="hidden md:grid grid-cols-[1.2fr_2fr_2fr] bg-slate-900 text-white font-bold">
            <div className="py-6 px-8 flex items-center text-emerald-400">管理逻辑</div>
            <div className="py-6 px-12 border-l border-white/10 opacity-70">普通相册</div>
            <div className="py-6 px-12 border-l border-white/10 bg-emerald-600">芯图相册</div>
          </div>

          <ComparisonRow 
            title="内容纯净度"
            icon={<Filter />}
            systemText="全盘无差别扫描，相册里充斥着应用广告图、截图与缩略图。"
            xintuText="智能筛选摄影内容。精准排除非照片干扰，让相册只展示美好的时刻。"
          />
          <ComparisonRow 
            title="查找效率"
            icon={<Search />}
            systemText="分类单一且浅层。在数万张照片中精准查找特定风格的照片极其困难。"
            xintuText="12维多维索引。通过时间、颜色、光圈、内容等参数实现毫秒级精准定位。"
          />
          <ComparisonRow 
            title="数据安全性"
            icon={<ShieldCheck />}
            systemText="往往伴随云端同步。隐私数据可能存在被分析或外泄的潜在隐患。"
            xintuText="100% 本地闭环处理。不上传、不备份、不联网，您的照片只属于您。"
          />
          <ComparisonRow 
            title="管理自主权"
            icon={<Settings2 />}
            systemText="由系统强制决定扫描范围。用户无法自主控制管理边界，显得笨重。"
            xintuText="按需扫描特定目录。您可以根据存储习惯自主定义管理范围，更轻快。"
          />
        </div>
      </div>
    </section>
  );
};

// Footer 已移除，使用公共组件（通过 components-loader.js 加载）

const App: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Navbar 和 Footer 已移除，使用公共组件（通过 components-loader.js 加载） */}
      <Hero />
      <Features />
      <Dimensions />
      <Comparison />
      
      {/* Download Section */}
      <section id="download" className="py-24 bg-emerald-600 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-1/3 h-full bg-emerald-500/20 -skew-x-12 translate-x-1/2"></div>
        <div className="max-w-7xl mx-auto px-6 relative z-10 text-center text-white">
          <h2 className="text-4xl font-black mb-8">开始体验纯净有序的相册</h2>
          <p className="text-emerald-100 mb-12 text-lg font-medium">无需注册，即下即用，让你的照片焕然一新</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <a 
              href="/download.py?type=portable"
              className="group px-8 py-6 bg-white text-emerald-600 rounded-2xl font-bold shadow-2xl hover:scale-105 transition-all flex flex-col items-center justify-center active:scale-95"
            >
              <Download className="mb-3 w-8 h-8 group-hover:animate-bounce" />
              <span className="text-lg">下载便携版 (Windows)</span>
              <span className="text-sm text-emerald-500 mt-1">便携版 · 无需安装</span>
            </a>
            <a 
              href="/download.py?type=setup"
              className="group px-8 py-6 bg-white text-emerald-600 rounded-2xl font-bold shadow-2xl hover:scale-105 transition-all flex flex-col items-center justify-center active:scale-95"
            >
              <Monitor className="mb-3 w-8 h-8 group-hover:animate-pulse" />
              <span className="text-lg">下载安装版 (Windows)</span>
              <span className="text-sm text-emerald-500 mt-1">安装版 · 自动安装</span>
            </a>
            <a 
              href="/download.py?type=android"
              className="group px-8 py-6 bg-emerald-800 text-white rounded-2xl font-bold shadow-2xl hover:bg-emerald-900 transition-all border border-emerald-400/30 flex flex-col items-center justify-center active:scale-95"
            >
              <Smartphone className="mb-3 w-8 h-8 group-hover:animate-bounce" />
              <span className="text-lg">下载 Android 版</span>
              <span className="text-sm text-emerald-200 mt-1">Android · 即装即用</span>
            </a>
            <a 
              href="https://apps.microsoft.com/detail/9MV2DHVG8952?hl=zh-cn&gl=cn"
              target="_blank"
              rel="noopener noreferrer"
              className="group px-8 py-6 bg-emerald-800 text-white rounded-2xl font-bold shadow-2xl hover:bg-emerald-900 transition-all border border-emerald-400/30 flex flex-col items-center justify-center active:scale-95"
            >
              <Monitor className="mb-3 w-8 h-8 group-hover:animate-pulse" />
              <span className="text-lg">微软应用市场下载</span>
              <span className="text-sm text-emerald-200 mt-1">自动更新 · 安全可靠</span>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default App;
