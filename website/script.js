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

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
    }
    
    lastScroll = currentScroll;
});

// 移动菜单切换
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// FAQ 折叠/展开
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    
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
});

// 截图标签切换
const tabButtons = document.querySelectorAll('.tab-btn');
const screenshotItems = document.querySelectorAll('.screenshot-item');

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

// 返回顶部按钮
const backToTopButton = document.querySelector('.back-to-top');

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

// 下载按钮点击事件追踪
const downloadButtons = document.querySelectorAll('a[href*=".exe"], a[download]');
downloadButtons.forEach(button => {
    button.addEventListener('click', () => {
        console.log('下载按钮被点击');
        // 这里可以添加统计代码，如 Google Analytics
        // gtag('event', 'download', { 'event_category': 'engagement' });
    });
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
    // 添加页面加载动画
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);

    // 自动打开第一个 FAQ（可选）
    // if (faqItems.length > 0) {
    //     faqItems[0].classList.add('active');
    // }

    // 获取最新下载文件信息
    fetchLatestFileInfo();
});

// 获取最新下载文件信息
function fetchLatestFileInfo() {
    fetch('download.php?info=1')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 提取版本号（如果文件名包含版本号）
                const versionMatch = data.filename.match(/(\d+\.\d+\.\d+)/);
                const version = versionMatch ? 'v' + versionMatch[1] : 'v1.0.0';
                
                // 更新所有显示文件信息的元素
                const versionElements = document.querySelectorAll('#file-version, #file-version-2');
                versionElements.forEach(el => {
                    if (el.id === 'file-version-2') {
                        el.textContent = '版本 ' + version;
                    } else {
                        el.textContent = version;
                    }
                });
                
                const sizeElements = document.querySelectorAll('#file-size, #file-size-2');
                sizeElements.forEach(el => {
                    el.textContent = data.sizeFormatted;
                });
                
                // 更新下载按钮的title提示
                const downloadButtons = document.querySelectorAll('.download-btn');
                downloadButtons.forEach(btn => {
                    btn.title = `下载: ${data.filename} (${data.sizeFormatted})`;
                });
                
                console.log('最新下载文件:', data.filename, data.sizeFormatted);
            }
        })
        .catch(error => {
            console.error('获取文件信息失败:', error);
            // 如果获取失败，显示默认信息
            const sizeElements = document.querySelectorAll('#file-size, #file-size-2');
            sizeElements.forEach(el => {
                el.textContent = '点击下载';
            });
        });
}

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
    if (e.key === 'Escape' && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
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

// 自动获取最新下载文件信息
async function updateDownloadInfo() {
    try {
        // 智能检测最新文件 - 尝试多个可能的文件名
        const possibleFiles = [
            'xtxc202510151254.zip',  // 最新文件
            'xtxc202510111614.zip',  // 备用文件
            '芯图相册-智能分类，便捷管理，仅你可见 1.0.0.exe'  // exe文件作为最后备用
        ];
        
        let latestFile = null;
        
        // 尝试检测最新文件
        for (const filename of possibleFiles) {
            try {
                const response = await fetch(`dist/${filename}`, { method: 'HEAD' });
                if (response.ok) {
                    latestFile = {
                        filename: filename,
                        path: `dist/${filename}`,
                        size: 275 * 1024 * 1024, // 默认大小
                        version: 'v1.0.0'
                    };
                    break;
                }
            } catch (e) {
                continue;
            }
        }
        
        // 如果没找到任何文件，使用默认的
        if (!latestFile) {
            latestFile = {
                filename: possibleFiles[0],
                path: `dist/${possibleFiles[0]}`,
                size: 275 * 1024 * 1024,
                version: 'v1.0.0'
            };
        }
        
        // 更新所有下载按钮的链接
        const downloadButtons = document.querySelectorAll('.download-btn');
        downloadButtons.forEach(btn => {
            btn.href = latestFile.path;
            btn.download = latestFile.filename;
        });
        
        // 格式化文件大小
        const sizeFormatted = formatBytes(latestFile.size);
        
        // 更新页面上的文件信息
        const versionElement = document.getElementById('file-version');
        const versionElement2 = document.getElementById('file-version-2');
        const sizeElement = document.getElementById('file-size');
        const sizeElement2 = document.getElementById('file-size-2');
        
        if (versionElement) versionElement.textContent = latestFile.version;
        if (versionElement2) versionElement2.textContent = '版本 ' + latestFile.version;
        if (sizeElement) sizeElement.textContent = sizeFormatted;
        if (sizeElement2) sizeElement2.textContent = sizeFormatted;
        
        console.log('下载文件信息已更新:', latestFile);
    } catch (error) {
        console.error('获取下载文件信息失败:', error);
        // 如果获取失败，保持默认值
    }
}

// 格式化字节大小
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// 页面加载时更新下载信息
document.addEventListener('DOMContentLoaded', () => {
    updateDownloadInfo();
});

console.log('芯图相册官网已加载完成 🎉');

