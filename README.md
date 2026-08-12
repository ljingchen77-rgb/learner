# 刘靖臣的个人网站

部署在 GitHub Pages 上的静态个人主页与 Markdown 博客，聚焦核工程、磁约束核聚变、研究经历和学习记录。

## 本地预览

在本目录运行：

```powershell
python -m http.server 8000
```

访问 `http://localhost:8000/`。请勿直接双击 HTML 预览，因为浏览器会限制页面读取文章索引与 Markdown 文件。

## 增加研究经历

研究经历直接维护在首页文件 `index.html` 中。搜索：

```html
<section id="research">
```

在这个区块中，每段研究经历由“摘要”和“展开详情”两部分组成。复制下面的完整模板，放在已有研究经历的后面、`</section>` 前面：

```html
<div class="edu-item">
    <span class="edu-year">2026 – 2027</span>
    <strong>项目类型或职位</strong> — 研究项目标题<br>
    <span style="font-size: 13px; color: #999;">指导老师：姓名与职称</span>
</div>

<details class="research-details">
    <summary>查看详情</summary>
    <div class="research-body">
        <p><strong>研究方法：</strong>介绍使用的实验、建模或数据分析方法。</p>
        <p><strong>研究内容：</strong>介绍研究对象、负责的工作和核心问题。</p>
        <p><strong>主要结论：</strong>介绍结果、成果或目前得到的认识。</p>
    </div>
</details>
```

修改时注意：

- 每段经历的 `<div>`、`<details>` 和结束标签都要完整保留。
- 如果没有指导老师，可以删除第二行 `<span>`。
- 尚无结论的项目，可以把“主要结论”改成“当前进展”。
- 时间按从新到旧排列，更方便访客阅读。

保存后访问首页，点击“查看详情”检查内容是否能正常展开。

## 发布新文章

一篇文章需要同时新增 Markdown 正文，并在文章索引中登记。只创建 Markdown 文件不会自动显示在网站上。

1. 在 `blog/posts/` 新建 UTF-8 编码的 Markdown 文件，例如 `fusion-notes.md`。
2. 使用下面的文章模板编写正文：

```markdown
# 文章标题

**2026 年 7 月 20 日**

---

这里写文章导语。

## 第一个小标题

这里写正文，可以使用列表、链接和代码块。
```

3. 在 `blog/posts/posts.json` 数组最前面添加元数据：

```json
{
  "title": "文章标题",
  "date": "2026-07-20",
  "file": "posts/fusion-notes.md",
  "categories": ["聚变", "学习笔记"],
  "summary": "用于首页和博客列表的简短摘要。"
}
```

如果它不是索引中的最后一项，右花括号后必须有英文逗号：

```json
},
```

4. 本地检查以下内容：

   - 首页“最新文章”是否出现新文章。
   - 博客分类筛选是否包含新分类。
   - 点击标题后正文、标题和代码块是否正常显示。
   - `posts.json` 中是否有漏写或多写的逗号。

5. 提交并推送；GitHub Pages 会自动更新。

首页会自动读取 `posts.json` 中排在最前面的 3 篇文章，不需要再修改 `index.html`。想调整首页文章顺序，只需调整 `posts.json` 中各项的顺序。

## 最常修改的位置

| 想修改的内容 | 文件 |
| --- | --- |
| 姓名、简介、教育和研究经历 | `index.html` |
| 新文章正文 | `blog/posts/文章名.md` |
| 文章标题、日期、分类、摘要与排序 | `blog/posts/posts.json` |
| 博客标题和说明 | `blog/index.html` |
| 颜色、间距和页面外观 | `style.css` |

## 结构

- `index.html`：个人主页
- `blog/`：博客页面、脚本、文章索引和 Markdown 正文
- `blog.html`：旧博客地址兼容跳转页
- `style.css`：全站视觉与响应式样式
- `script.js`：主题与首页动效
- `blog/blog.js`：文章索引、分类、Markdown 渲染与评论
- `blog/posts/posts.json`：文章元数据
- `blog/posts/*.md`：文章正文
- `feed.xml`：博客 RSS 订阅源
- `sitemap.xml`：搜索引擎站点地图
- `404.html`：页面不存在时的提示页
- `en/index.html`：英文主页
- `assets/Liu-Jingchen-Resume.pdf`：由网站内容生成的中英文简历
- `tools/generate_resume.py`：简历 PDF 生成脚本
- `assets/Liu-Jingchen-Academic-Resume-CN.pdf`：联系导师使用的一页中文学术简历
- `tools/generate_academic_resume.py`：中文学术简历生成脚本
- `tools/academic_resume_data.json`：中文学术简历的结构化内容数据，后续优先在此维护经历、课程和荣誉

博客会自动提供文章搜索、分类筛选、阅读时间、正文目录及上一篇/下一篇导航。新增文章后，需要同步更新 `feed.xml`；如果新增独立页面，也需要将页面地址加入 `sitemap.xml`。

首页经历或技能发生变化后，请同步修改 `tools/generate_resume.py` 中的简历内容，并运行该脚本重新生成 PDF。
联系导师版简历的内容维护在 `tools/generate_academic_resume.py`，更新后需重新运行脚本生成 PDF。

Markdown 渲染依赖 Marked.js，HTML 清理由 DOMPurify 完成，评论使用 Utterances。这些资源通过 CDN 加载，完全离线时不可用。
