# 刘靖臣的个人网站

部署在 GitHub Pages 上的静态个人主页与 Markdown 博客，聚焦核工程、磁约束核聚变、研究经历和学习记录。

## 本地预览

在本目录运行：

```powershell
python -m http.server 8000
```

访问 `http://localhost:8000/`。请勿直接双击 HTML 预览，因为浏览器会限制页面读取文章索引与 Markdown 文件。

## 发布文章

1. 在 `blog/posts/` 新建 UTF-8 编码的 Markdown 文件，例如 `fusion-notes.md`。
2. 在 `blog/posts/posts.json` 数组开头添加元数据：

```json
{
  "title": "文章标题",
  "date": "2026-07-20",
  "file": "posts/fusion-notes.md",
  "categories": ["聚变", "学习笔记"],
  "summary": "用于首页和博客列表的简短摘要。"
}
```

3. 本地检查首页、分类筛选、正文和暗色模式。
4. 提交并推送；GitHub Pages 会自动更新。

## 结构

- `index.html`：个人主页
- `blog/`：博客页面、脚本、文章索引和 Markdown 正文
- `blog.html`：旧博客地址兼容跳转页
- `style.css`：全站视觉与响应式样式
- `script.js`：主题与首页动效
- `blog/blog.js`：文章索引、分类、Markdown 渲染与评论
- `blog/posts/posts.json`：文章元数据
- `blog/posts/*.md`：文章正文

Markdown 渲染依赖 Marked.js，HTML 清理由 DOMPurify 完成，评论使用 Utterances。这些资源通过 CDN 加载，完全离线时不可用。
