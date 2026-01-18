// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// 导航栏背景变化
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

if (navbar) {
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
        }
        
        lastScroll = currentScroll;
    });
}

// 移动菜单切换 - 侧边栏抽屉式
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');
const navOverlay = document.querySelector('.nav-overlay');

function toggleMobileMenu() {
    if (!navLinks || !mobileMenuToggle) return;
    const isActive = navLinks.classList.contains('active');
    navLinks.classList.toggle('active');
    mobileMenuToggle.classList.toggle('active');
    if (navOverlay) {
        navOverlay.classList.toggle('active');
    }
    // 防止背景滚动
    document.body.style.overflow = isActive ? '' : 'hidden';
}

function closeMobileMenu() {
    if (!navLinks || !mobileMenuToggle) return;
    navLinks.classList.remove('active');
    mobileMenuToggle.classList.remove('active');
    if (navOverlay) {
        navOverlay.classList.remove('active');
    }
    document.body.style.overflow = '';
}

if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMobileMenu();
    });
    
    // 点击遮罩层关闭菜单
    if (navOverlay) {
        navOverlay.addEventListener('click', closeMobileMenu);
    }
    
    // 点击菜单项后关闭菜单
    const navLinksItems = navLinks.querySelectorAll('a');
    navLinksItems.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
    
    // ESC键关闭菜单
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            closeMobileMenu();
        }
    });
}

// FAQ 折叠/展开
const faqItems = document.querySelectorAll('.faq-item');

if (faqItems.length > 0) {
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // 关闭所有其他项
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // 切换当前项
                if (isActive) {
                    item.classList.remove('active');
                } else {
                    item.classList.add('active');
                }
            });
        }
    });
}

// 截图标签切换（仅在存在这些元素时执行）
const tabButtons = document.querySelectorAll('.tab-btn');
const screenshotItems = document.querySelectorAll('.screenshot-item');

if (tabButtons.length > 0 && screenshotItems.length > 0) {
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // 更新按钮状态
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // 更新截图显示
            screenshotItems.forEach(item => {
                if (item.getAttribute('data-content') === targetTab) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        });
    });
}

// 返回顶部按钮
const backToTopButton = document.querySelector('.back-to-top');

if (backToTopButton) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 交叉观察器 - 滚动动画
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// 为需要动画的元素添加初始样式和观察
const animateElements = document.querySelectorAll('.feature-card, .pain-point-card, .step, .faq-item');
animateElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});

// 统计数字动画
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value + '%';
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// 当统计数字进入视口时开始动画
const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
            entry.target.classList.add('animated');
            const targetValue = 90;
            animateValue(entry.target, 0, targetValue, 2000);
        }
    });
}, { threshold: 0.5 });

// 只对特定的统计数字应用动画
const statNumbers = document.querySelectorAll('.hero-stats .stat-number');
statNumbers.forEach(stat => {
    if (stat.textContent.includes('%')) {
        statObserver.observe(stat);
    }
});

// 防止链接默认行为（对于占位符链接）
const placeholderLinks = document.querySelectorAll('a[href="#contact"], a[href="#feedback"], a[href="#about"], a[href="#privacy"], a[href="#terms"]');
placeholderLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        alert('此功能即将推出，敬请期待！');
    });
});

// 图片懒加载（如果浏览器不支持原生懒加载）
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // 使用 Intersection Observer 实现懒加载
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(img => imageObserver.observe(img));
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', () => {
    // 确保页面可见（移除可能导致页面隐藏的样式）
    try {
        // 立即确保body可见
        if (document.body) {
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.style.display = '';
        }
        
        // 可选：添加淡入动画（仅在需要时）
        // document.body.style.opacity = '0';
        // setTimeout(() => {
        //     document.body.style.transition = 'opacity 0.5s ease-in';
        //     document.body.style.opacity = '1';
        // }, 100);
    } catch (error) {
        // 如果出错，确保页面仍然可见
        console.error('页面初始化出错:', error);
        if (document.body) {
            document.body.style.opacity = '1';
            document.body.style.visibility = 'visible';
            document.body.style.display = '';
        }
    }

    // 自动打开第一个 FAQ（可选）
    // if (faqItems.length > 0) {
    //     faqItems[0].classList.add('active');
    // }

    // 不再需要 fetchLatestFileInfo，因为 download.py 会自动处理
});

// fetchLatestFileInfo 函数已移除，因为 download.py 会自动处理最新文件

// 性能监控
window.addEventListener('load', () => {
    // 计算页面加载时间
    const loadTime = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
    console.log(`页面加载时间: ${loadTime}ms`);
});

// 处理表单提交（如果将来添加联系表单）
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        // 这里添加表单验证和提交逻辑
        console.log('表单已提交');
    });
});

// 键盘导航支持
document.addEventListener('keydown', (e) => {
    // ESC 键关闭移动菜单
    if (e.key === 'Escape' && navLinks && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        if (mobileMenuToggle) {
            mobileMenuToggle.classList.remove('active');
        }
        if (navOverlay) {
            navOverlay.classList.remove('active');
        }
        document.body.style.overflow = '';
    }
});

// 添加键盘焦点可见性
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-nav');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-nav');
});

// 检测系统暗色模式（为未来的暗色模式做准备）
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    console.log('用户偏好暗色模式');
    // 可以在这里添加暗色模式逻辑
}

// 监听暗色模式变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    const darkModeOn = e.matches;
    console.log(`暗色模式: ${darkModeOn ? '开启' : '关闭'}`);
});

// 复制到剪贴板功能（用于未来可能的分享功能）
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('复制失败:', err);
        }
        textArea.remove();
    }
}

// 导出函数供全局使用
window.xintuxiangce = {
    copyToClipboard,
    scrollToSection: (sectionId) => {
        const section = document.getElementById(sectionId);
        if (section) {
            const offsetTop = section.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }
};

console.log('芯图相册官网已加载完成 🎉');

// 调试工具：在微信或 ?debug=1 时在页面左下角显示日志
const __XT_VERSION = 'wx-intercept-20251030';
function __xt_shouldDebug() {
    try {
        const q = new URLSearchParams(location.search);
        if (q.get('debug') === '1') return true; // 仅当显式指定时显示调试面板
    } catch (e) {}
    return false;
}
function __xt_log(msg) {
    try {
        console.log('[XT]', msg);
        if (!__xt_shouldDebug()) return;
        let panel = document.getElementById('xt-debug-panel');
        if (!panel) {
            panel = document.createElement('div');
            panel.id = 'xt-debug-panel';
            panel.style.position = 'fixed';
            panel.style.left = '8px';
            panel.style.bottom = '8px';
            panel.style.maxWidth = '80vw';
            panel.style.maxHeight = '40vh';
            panel.style.overflow = 'auto';
            panel.style.background = 'rgba(0,0,0,0.7)';
            panel.style.color = '#0f0';
            panel.style.fontSize = '12px';
            panel.style.lineHeight = '1.4';
            panel.style.padding = '6px 8px';
            panel.style.borderRadius = '6px';
            panel.style.zIndex = '10000';
            panel.style.pointerEvents = 'none';
            panel.textContent = `[XT ${__XT_VERSION}]`;
            document.addEventListener('DOMContentLoaded', () => {
                document.body.appendChild(panel);
            });
            // 若 DOM 已就绪
            if (document.readyState !== 'loading' && document.body) {
                document.body.appendChild(panel);
            }
        }
        const line = document.createElement('div');
        const now = new Date();
        const ts = now.toLocaleTimeString();
        line.textContent = `${ts} - ${msg}`;
        panel.appendChild(line);
    } catch (e) {}
}
__xt_log('script loaded');

// 微信内置浏览器下载拦截与指引
(function () {
    try {
        const ua = navigator.userAgent || '';
        const isWeChat = ua.indexOf('MicroMessenger') !== -1;
        __xt_log(`UA=${ua}`);
        __xt_log(`isWeChat=${isWeChat}`);
        if (!isWeChat) return;

        const overlay = document.createElement('div');
        overlay.id = 'wx-download-overlay';
        overlay.style.position = 'fixed';
        overlay.style.left = '0';
        overlay.style.top = '0';
        overlay.style.right = '0';
        overlay.style.bottom = '0';
        overlay.style.background = 'rgba(0,0,0,0.75)';
        overlay.style.display = 'none';
        overlay.style.zIndex = '99999'; // 提高 z-index，确保在最上层
        overlay.style.backdropFilter = 'blur(4px)';
        overlay.style.alignItems = 'center';
        overlay.style.justifyContent = 'center';
        overlay.style.padding = '20px';
        overlay.style.overflow = 'auto'; // 确保内容可滚动

        const panel = document.createElement('div');
        panel.style.position = 'relative';
        panel.style.width = 'min(92%, 400px)';
        panel.style.background = '#fff';
        panel.style.borderRadius = '16px';
        panel.style.boxShadow = '0 20px 60px rgba(0,0,0,0.3)';
        panel.style.padding = '32px 24px 24px';
        panel.style.textAlign = 'center';
        panel.style.maxWidth = '400px';

        // 图标提示区域
        const iconArea = document.createElement('div');
        iconArea.style.marginBottom = '20px';
        iconArea.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 12px;">🌐</div>
            <div style="font-size: 32px; color: #2563eb; margin-bottom: 8px;">📱</div>
        `;

        const title = document.createElement('div');
        title.textContent = '请在系统浏览器中打开';
        title.style.fontSize = '20px';
        title.style.fontWeight = '600';
        title.style.color = '#111';
        title.style.marginBottom = '12px';

        const desc = document.createElement('div');
        desc.innerHTML = `
            <p style="font-size: 14px; color: #666; line-height: 1.6; margin-bottom: 16px;">
                微信浏览器无法直接下载文件，请使用系统浏览器打开下载链接。
            </p>
            <div style="background: #f0f7ff; border-left: 3px solid #2563eb; padding: 12px; margin-bottom: 20px; text-align: left; border-radius: 4px;">
                <div style="font-size: 13px; color: #2563eb; font-weight: 600; margin-bottom: 6px;">操作步骤：</div>
                <div style="font-size: 13px; color: #444; line-height: 1.8;">
                    1. 点击下方"在浏览器中打开"按钮<br>
                    2. 选择"在浏览器中打开"或"在Safari中打开"<br>
                    3. 在浏览器中完成下载
                </div>
            </div>
        `;
        desc.style.fontSize = '14px';
        desc.style.color = '#444';
        desc.style.lineHeight = '1.6';

        const actions = document.createElement('div');
        actions.style.display = 'flex';
        actions.style.flexDirection = 'column';
        actions.style.gap = '12px';

        // 在浏览器中打开按钮（主要按钮）
        const openInBrowserBtn = document.createElement('a');
        openInBrowserBtn.textContent = '在浏览器中打开';
        openInBrowserBtn.style.padding = '14px 24px';
        openInBrowserBtn.style.border = 'none';
        openInBrowserBtn.style.background = 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)';
        openInBrowserBtn.style.color = '#fff';
        openInBrowserBtn.style.borderRadius = '8px';
        openInBrowserBtn.style.cursor = 'pointer';
        openInBrowserBtn.style.fontSize = '16px';
        openInBrowserBtn.style.fontWeight = '600';
        openInBrowserBtn.style.textDecoration = 'none';
        openInBrowserBtn.style.display = 'block';
        openInBrowserBtn.style.transition = 'all 0.3s ease';
        openInBrowserBtn.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
        
        // 悬停效果
        openInBrowserBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 6px 16px rgba(37, 99, 235, 0.4)';
        });
        openInBrowserBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
        });

        // 复制链接按钮（次要按钮）
        const copyBtn = document.createElement('button');
        copyBtn.textContent = '复制下载链接';
        copyBtn.style.padding = '12px 24px';
        copyBtn.style.border = '1px solid #e5e7eb';
        copyBtn.style.background = '#fff';
        copyBtn.style.color = '#666';
        copyBtn.style.borderRadius = '8px';
        copyBtn.style.cursor = 'pointer';
        copyBtn.style.fontSize = '14px';
        copyBtn.style.transition = 'all 0.3s ease';

        copyBtn.addEventListener('mouseenter', function() {
            this.style.background = '#f9fafb';
            this.style.borderColor = '#2563eb';
            this.style.color = '#2563eb';
        });
        copyBtn.addEventListener('mouseleave', function() {
            this.style.background = '#fff';
            this.style.borderColor = '#e5e7eb';
            this.style.color = '#666';
        });

        // 关闭按钮
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '取消';
        closeBtn.style.padding = '10px 20px';
        closeBtn.style.border = 'none';
        closeBtn.style.background = 'transparent';
        closeBtn.style.color = '#999';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.fontSize = '13px';
        closeBtn.style.marginTop = '8px';

        actions.appendChild(openInBrowserBtn);
        actions.appendChild(copyBtn);
        actions.appendChild(closeBtn);

        panel.appendChild(iconArea);
        panel.appendChild(title);
        panel.appendChild(desc);
        panel.appendChild(actions);
        overlay.appendChild(panel);
        
        // 确保 body 存在后再添加 overlay
        function appendOverlay() {
            if (document.body) {
                document.body.appendChild(overlay);
            } else {
                // 如果 body 还不存在，等待 DOM 加载
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', appendOverlay);
                } else {
                    // 如果已经加载完成但 body 还不存在，延迟一下
                    setTimeout(appendOverlay, 100);
                }
            }
        }
        appendOverlay();

        let currentDownloadHref = '';

        function openOverlay(href) {
            currentDownloadHref = href;
            // 设置"在浏览器中打开"按钮的链接
            openInBrowserBtn.href = href;
            openInBrowserBtn.target = '_blank';
            // 尝试添加 rel="external" 以提示浏览器在新窗口打开
            openInBrowserBtn.setAttribute('rel', 'external');
            
            // 确保 overlay 存在且已添加到 DOM
            if (!overlay.parentNode && document.body) {
                document.body.appendChild(overlay);
            }
            
            // 确保 overlay 显示在最上层
            overlay.style.display = 'flex';
            overlay.style.zIndex = '99999';
            overlay.style.visibility = 'visible';
            overlay.style.opacity = '1';
            
            // 防止 body 滚动
            if (document.body) {
                document.body.style.overflow = 'hidden';
            }
            
            __xt_log('overlay open: ' + href);
        }

        function closeOverlay() {
            overlay.style.display = 'none';
            // 恢复 body 滚动
            document.body.style.overflow = '';
        }

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeOverlay();
        });
        closeBtn.addEventListener('click', closeOverlay);

        copyBtn.addEventListener('click', async () => {
            try {
                await (window.xintuxiangce && window.xintuxiangce.copyToClipboard
                    ? window.xintuxiangce.copyToClipboard(currentDownloadHref)
                    : navigator.clipboard.writeText(currentDownloadHref));
                copyBtn.textContent = '✓ 已复制';
                copyBtn.style.color = '#10b981';
                setTimeout(() => {
                    copyBtn.textContent = '复制下载链接';
                    copyBtn.style.color = '#666';
                }, 2000);
            } catch (err) {
                console.error(err);
                copyBtn.textContent = '复制失败';
                copyBtn.style.color = '#ef4444';
                setTimeout(() => {
                    copyBtn.textContent = '复制下载链接';
                    copyBtn.style.color = '#666';
                }, 2000);
            }
        });

        // 检查是否是下载链接
        function isDownloadLink(href) {
            if (!href) return false;
            return href.includes('download.py') || 
                   href.includes('dist/') || 
                   /\.(exe|zip|apk)$/i.test(href) ||
                   href.includes('download');
        }

        // 处理下载链接点击
        function handleDownloadClick(e, target) {
            const href = target.getAttribute('href') || target.href || '';
            if (!isDownloadLink(href)) {
                __xt_log(`not a download link: ${href}`);
                return false;
            }
            
            // 彻底阻止默认行为和事件传播（必须在最开始就阻止）
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            e.cancelBubble = true; // IE 兼容
            e.returnValue = false; // 阻止默认行为（IE 兼容）
            
            let absolute = href.startsWith('http') ? href : (new URL(href, window.location.href)).href;
            
            // 如果是移动端（Android），且链接是下载链接，自动改为Android版本
            const ua = navigator.userAgent || '';
            const isAndroid = /android/i.test(ua);
            if (isAndroid && absolute.includes('download.py')) {
                // 将 type 参数改为 android
                if (absolute.includes('type=')) {
                    absolute = absolute.replace(/[?&]type=[^&]*/, '');
                    absolute += (absolute.includes('?') ? '&' : '?') + 'type=android';
                } else {
                    absolute += (absolute.includes('?') ? '&' : '?') + 'type=android';
                }
                __xt_log(`mobile detected, changed to android: ${absolute}`);
            }
            
            openOverlay(absolute);
            __xt_log(`intercept: ${absolute}`);
            return false;
        }

        // 事件委托：在 document 级别拦截所有下载链接的点击
        function setupEventDelegation() {
            // 拦截所有可能触发下载的事件，按优先级排序
            // touchstart 和 mousedown 在最前面，可以最早拦截
            const events = ['touchstart', 'mousedown', 'click', 'touchend', 'pointerup'];
            
            events.forEach(eventType => {
                document.addEventListener(eventType, function(e) {
                    // 查找点击的目标元素及其父元素
                    let target = e.target;
                    let attempts = 0;
                    const maxAttempts = 10; // 增加查找层数
                    
                    while (target && target !== document && attempts < maxAttempts) {
                        // 检查是否是链接元素
                        if (target.tagName === 'A') {
                            const href = target.getAttribute('href') || target.href || '';
                            if (isDownloadLink(href)) {
                                __xt_log(`intercept ${eventType} on ${href}`);
                                handleDownloadClick(e, target);
                                return;
                            }
                        }
                        target = target.parentElement;
                        attempts++;
                    }
                }, { capture: true, passive: false });
            });
            
            __xt_log('event delegation setup done');
        }

        // 拦截已存在的下载按钮
        function interceptExistingLinks() {
            const candidates = document.querySelectorAll('a[href*="download.py"], a[href*="dist/"], a[href$=".exe"], a[href$=".zip"], a[href$=".apk"], a[download]');
            __xt_log(`existing candidates=${candidates.length}`);
            
            candidates.forEach(a => {
                // 移除可能存在的旧事件监听器，添加新的
                const events = ['click', 'touchend', 'touchstart', 'pointerup'];
                events.forEach(eventType => {
                    a.addEventListener(eventType, function(e) {
                        handleDownloadClick(e, a);
                    }, { capture: true, passive: false });
                });
            });
        }

        // 使用 MutationObserver 监听 DOM 变化，拦截动态添加的下载按钮
        function setupMutationObserver() {
            const observer = new MutationObserver(function(mutations) {
                let shouldIntercept = false;
                mutations.forEach(function(mutation) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            // 检查新添加的节点是否是下载链接
                            if (node.tagName === 'A' && isDownloadLink(node.href)) {
                                shouldIntercept = true;
                            }
                            // 检查新添加的节点内部是否有下载链接
                            const links = node.querySelectorAll && node.querySelectorAll('a[href*="download.py"], a[href*="dist/"], a[href$=".exe"], a[href$=".zip"], a[href$=".apk"], a[download]');
                            if (links && links.length > 0) {
                                shouldIntercept = true;
                            }
                        }
                    });
                });
                
                if (shouldIntercept) {
                    setTimeout(interceptExistingLinks, 100);
                }
            });

            observer.observe(document.body || document.documentElement, {
                childList: true,
                subtree: true
            });
            
            __xt_log('mutation observer setup done');
        }

        // 初始化拦截
        setupEventDelegation();
        
        // 等待 DOM 加载完成后拦截已存在的链接
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                interceptExistingLinks();
                setupMutationObserver();
            });
        } else {
            interceptExistingLinks();
            setupMutationObserver();
        }
        
        __xt_log('intercept init done');
    } catch (e) {
        console.error('WeChat download intercept failed:', e);
        __xt_log('intercept init error');
    }
})();

