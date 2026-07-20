let allPosts=[];
let activeCategory='全部';
let searchQuery='';
const listView=document.getElementById('post-list');
const contentView=document.getElementById('post-content');
const itemsContainer=document.getElementById('post-items');
const filterContainer=document.getElementById('category-filter');
const bodyContainer=document.getElementById('post-body');
const commentsContainer=document.getElementById('comments-container');
const backBtn=document.getElementById('back-btn');
const searchInput=document.getElementById('post-search');
const metaContainer=document.getElementById('article-meta');
const tocContainer=document.getElementById('article-toc');
const navigationContainer=document.getElementById('post-navigation');

fetch('posts/posts.json').then(response=>{if(!response.ok)throw new Error('文章列表加载失败');return response.json()}).then(posts=>{allPosts=posts;renderCategories();applyFilters();const file=new URLSearchParams(location.search).get('post');if(file)loadPost(file)}).catch(error=>showStatus(itemsContainer,`⚠ ${error.message}`));

searchInput.addEventListener('input',event=>{searchQuery=event.target.value.trim().toLowerCase();applyFilters()});

function showStatus(container,message){container.replaceChildren();const node=document.createElement('p');node.className='status-message';node.textContent=message;container.appendChild(node)}

function renderCategories(){filterContainer.replaceChildren();const categories=['全部',...new Set(allPosts.flatMap(post=>post.categories||[]))];categories.forEach((category,index)=>{const button=document.createElement('button');button.className=`category-tag${index===0?' active':''}`;button.type='button';button.textContent=category;button.setAttribute('aria-pressed',String(index===0));button.addEventListener('click',()=>{activeCategory=category;filterContainer.querySelectorAll('button').forEach(item=>{const active=item===button;item.classList.toggle('active',active);item.setAttribute('aria-pressed',String(active))});applyFilters()});filterContainer.appendChild(button)})}

function applyFilters(){const filtered=allPosts.filter(post=>{const inCategory=activeCategory==='全部'||(post.categories||[]).includes(activeCategory);const haystack=[post.title,post.summary,...(post.categories||[])].join(' ').toLowerCase();return inCategory&&haystack.includes(searchQuery)});renderPosts(filtered)}

function renderPosts(posts){itemsContainer.replaceChildren();if(!posts.length)return showStatus(itemsContainer,'没有找到匹配的文章。');posts.forEach(post=>{const article=document.createElement('article'),meta=document.createElement('div'),heading=document.createElement('h3'),link=document.createElement('a'),summary=document.createElement('p');article.className='post-item';meta.className='post-meta';meta.textContent=post.date;(post.categories||[]).forEach(category=>{const tag=document.createElement('span');tag.className='tag';tag.textContent=category;meta.append(' ',tag)});link.href=`?post=${encodeURIComponent(post.file)}`;link.textContent=post.title;heading.appendChild(link);summary.className='post-summary';summary.textContent=post.summary;article.append(meta,heading,summary);itemsContainer.appendChild(article)})}

function loadPost(file){if(!/^posts\/[\w.-]+\.md$/.test(file))return showStatus(itemsContainer,'文章地址无效。');listView.classList.add('hidden');contentView.classList.add('active');scrollTo(0,0);showStatus(bodyContainer,'正在读取文章…');fetch(file).then(response=>{if(!response.ok)throw new Error('文章加载失败');return response.text()}).then(markdown=>{const title=markdown.split('\n')[0].replace(/^#\s*/,'');const rendered=marked.parse(markdown);bodyContainer.innerHTML=window.DOMPurify?DOMPurify.sanitize(rendered):rendered;document.title=`${title} · 刘靖臣`;renderArticleTools(file,markdown);loadComments()}).catch(error=>showStatus(bodyContainer,`⚠ ${error.message}`))}

function renderArticleTools(file,markdown){const words=markdown.replace(/[#*`>\[\]()_-]/g,'').replace(/\s+/g,'').length;const minutes=Math.max(1,Math.ceil(words/400));const post=allPosts.find(item=>item.file===file);metaContainer.textContent=`${post?.date||''} · 约 ${minutes} 分钟阅读`;
    const headings=[...bodyContainer.querySelectorAll('h2,h3')];tocContainer.replaceChildren();tocContainer.hidden=!headings.length;if(headings.length){const label=document.createElement('strong');label.textContent='本文目录';tocContainer.appendChild(label);headings.forEach((heading,index)=>{heading.id=`section-${index+1}`;const link=document.createElement('a');link.href=`#${heading.id}`;link.textContent=heading.textContent;if(heading.tagName==='H3')link.className='toc-sub';tocContainer.appendChild(link)})}
    navigationContainer.replaceChildren();const index=allPosts.findIndex(item=>item.file===file);appendNavLink(allPosts[index-1],'上一篇');appendNavLink(allPosts[index+1],'下一篇')}

function appendNavLink(post,label){if(!post)return;const link=document.createElement('a');link.href=`?post=${encodeURIComponent(post.file)}`;const small=document.createElement('span');small.textContent=label;const title=document.createElement('strong');title.textContent=post.title;link.append(small,title);navigationContainer.appendChild(link)}

function showListView(){contentView.classList.remove('active');listView.classList.remove('hidden');history.pushState({},'', './');document.title='博客 · 刘靖臣';commentsContainer.replaceChildren();tocContainer.replaceChildren();navigationContainer.replaceChildren()}
backBtn.addEventListener('click',event=>{event.preventDefault();showListView()});
addEventListener('popstate',()=>{const file=new URLSearchParams(location.search).get('post');if(file)loadPost(file);else showListView()});

function loadComments(){commentsContainer.replaceChildren();const script=document.createElement('script');script.src='https://utteranc.es/client.js';script.setAttribute('repo','ljingchen77-rgb/learner');script.setAttribute('issue-term','pathname');script.setAttribute('theme',document.body.classList.contains('dark-mode')?'github-dark':'github-light');script.setAttribute('crossorigin','anonymous');script.async=true;commentsContainer.appendChild(script)}
