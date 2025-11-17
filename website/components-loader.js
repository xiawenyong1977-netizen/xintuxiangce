/**
 * 公共组件加载器
 * 用于动态加载导航栏和底部栏组件
 */

(function() {
    'use strict';

    // 使用绝对路径，不需要路径检测
    // 组件路径从网站根目录开始：/components/
    function getComponentPath() {
        return '/components/';
    }

    // 所有链接已使用绝对路径，不需要调整
    function adjustPaths(html) {
        // 组件中的链接已全部使用绝对路径（如 /index.html, /faq.html）
        // 因此不需要根据页面深度调整路径
        return html;
    }

    // 加载组件
    function loadComponent(componentName, targetSelector, insertPosition = 'afterbegin') {
        const target = document.querySelector(targetSelector);
        if (!target) {
            console.warn(`目标元素 ${targetSelector} 未找到`);
            return;
        }

        const componentPath = getComponentPath() + componentName + '.html';
        
        // 添加时间戳和随机数防止缓存（双重保险）
        const cacheBuster = '?v=' + Date.now() + '&r=' + Math.random().toString(36).substr(2, 9);
        const fullPath = componentPath + cacheBuster;
        
        console.log(`正在加载组件: ${componentName}, 路径: ${fullPath}`);
        
        fetch(fullPath)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                // 调整HTML中的相对链接路径
                html = adjustPaths(html);
                
                // 插入HTML
                if (insertPosition === 'afterbegin') {
                    target.insertAdjacentHTML('afterbegin', html);
                } else if (insertPosition === 'beforeend') {
                    target.insertAdjacentHTML('beforeend', html);
                }
                
                console.log(`组件 ${componentName} 加载成功`);
                
                // 如果是导航栏，需要重新初始化移动菜单
                if (componentName === 'navbar') {
                    // 延迟初始化，确保DOM已更新
                    setTimeout(initMobileMenu, 10);
                }
            })
            .catch(error => {
                console.error(`加载组件 ${componentName} 失败:`, error);
                console.error(`尝试的路径: ${fullPath}`);
            });
    }

    // 初始化移动菜单（在组件加载后调用）
    function initMobileMenu() {
        const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
        const navLinks = document.querySelector('.nav-links');
        const navOverlay = document.querySelector('.nav-overlay');

        if (mobileMenuToggle && navLinks) {
            // 移除旧的事件监听器（如果存在）
            const newToggle = mobileMenuToggle.cloneNode(true);
            mobileMenuToggle.parentNode.replaceChild(newToggle, mobileMenuToggle);

            // 添加新的事件监听器
            newToggle.addEventListener('click', function() {
                const isActive = navLinks.classList.contains('active');
                navLinks.classList.toggle('active');
                newToggle.classList.toggle('active');
                if (navOverlay) {
                    navOverlay.classList.toggle('active');
                }
                document.body.style.overflow = isActive ? '' : 'hidden';
            });

            // 点击遮罩层关闭菜单
            if (navOverlay) {
                navOverlay.addEventListener('click', function() {
                    navLinks.classList.remove('active');
                    newToggle.classList.remove('active');
                    navOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                });
            }
        }
    }

    // 页面加载完成后加载组件
    function initComponents() {
        // 确保body元素存在
        if (!document.body) {
            // 如果body还不存在，等待一下
            setTimeout(initComponents, 10);
            return;
        }
        
        console.log('开始加载组件');
        
        // 导航栏插入到body开始
        loadComponent('navbar', 'body', 'afterbegin');
        // 底部栏插入到body结束
        loadComponent('footer', 'body', 'beforeend');
    }

    // 使用多种方式确保在合适的时机加载
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initComponents);
    } else if (document.body) {
        // 如果body已经存在，立即执行
        initComponents();
    } else {
        // 如果body还不存在，等待DOMContentLoaded
        document.addEventListener('DOMContentLoaded', initComponents);
    }
})();

