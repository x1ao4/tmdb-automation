# tmdb-automation
使用 tmdb-automation 可以利用 selenium 通过网页自动化实现自动向 TMDB 添加剧集信息或封面图片。由于 TMDB 不支持通过 API 向网站添加内容，所以我选择了使用 selenium 来实现这个功能。tmdb-automation 共包含两个脚本，auto-add-episodes 可以用来添加剧集，auto-add-covers 可以用来添加剧集封面。

## auto-add-episodes
### 运行条件
- 操作系统为 Windows、MacOS 或 Linux。
- 安装了 Python 3.0 或更高版本。
- 安装了必要的第三方库：selenium。
- 安装了 Chrome 浏览器和对应版本的 ChromeDriver。
- 有可用的 TMDB 账号。

### 使用方法
1. 将仓库克隆或下载到计算机上的一个目录中。
2. 根据需要，修改脚本中的参数：TMDB_USERNAME、TMDB_PASSWORD、EPISODES_URL、DATA_FILE 和 LANGUAGE_CODE。
   - TMDB_USERNAME：您的 TMDB 用户名。
   - TMDB_PASSWORD：您的 TMDB 用户密码。
   - EPISODES_URL：您要添加剧集的网址。（例如：`https://www.themoviedb.org/tv/229116-dust/season/8/edit?active_nav_item=episodes`，需要是具体某一季的集的编辑页面的完整地址）
   - DATA_FILE：您存储剧集信息的文本文件路径。（文本每一行代表一集的信息，需要包含五个由 `;` 分隔的字段，分别表示集编号、播出日期、时长、名字和分集剧情。）
   - LANGUAGE_CODE：您添加内容的语言代码。（例如：`zh-CN` 表示汉语，`en-US` 表示英语，以 TMDB 编辑页面显示的语言代码为准）
3. 修改 `start.command (Mac)` 或 `start.bat (Win)` 中的路径，以指向您存放 `auto-add-episodes.py` 脚本的目录。
4. 双击运行 `start.command` 或 `start.bat` 脚本以执行 `auto-add-episodes.py` 脚本。
5. 脚本会自动打开新的 Chrome 浏览器窗口，自动登录到 TMDB 网站，并根据提供的剧集信息添加新的剧集。若提供的剧集信息中有已经存在于 TMDB 上的剧集，脚本将跳过这些剧集并显示相应的提示信息，然后继续添加其他剧集。当所有剧集信息都处理完成后，脚本将显示成功添加的剧集数和失败的剧集数（如果有）。

### 注意事项
- 请确保您拥有合法的 TMDB 帐户，并且具有足够的权限执行所需的操作。
- 使用脚本时，请确保您的网络连接正常，并且 TMDB 网站可以正常访问。
- 请确保设置的 `LANGUAGE_CODE` 与您提供的剧集信息的文本语言一致。
- 请确保 TMDB 账户的语言偏好设置与您设置的 `LANGUAGE_CODE` 一致。
- 请确保提供的剧集信息文本格式与脚本中所述的格式及你的语言偏好一致。不同的语言对 `播出日期` 的格式要求可能不同，当语言为 `汉语` 时日期格式为 `YYYY/MM/DD` 例如 `2023/1/20`，当语言为 `英语` 时日期格式为 `MM/DD/YYYY` 例如 `1/20/2023`，请根据你的语言使用对应的格式。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。

## auto-add-covers
### 运行条件
- 操作系统为 MacOS。
- 安装了 Python 3.0 或更高版本。
- 安装了必要的第三方库：selenium。
- 安装了 Chrome 浏览器和对应版本的 ChromeDriver。
- 有可用的 TMDB 账号。

### 使用方法
1. 将仓库克隆或下载到计算机上的一个目录中。
2. 根据需要，修改脚本中的参数：TMDB_USERNAME、TMDB_PASSWORD、EPISODES_URL、IMAGE_FOLDER 和 LANGUAGE。
   - TMDB_USERNAME：您的 TMDB 用户名。
   - TMDB_PASSWORD：您的 TMDB 用户密码。
   - EPISODES_URL：您要添加剧集封面图片的网址。（例如：`https://www.themoviedb.org/tv/229116-dust/season/0/episode/1/images/backdrops`，可以是您要上传的季中任意一集的剧照页面）
   - IMAGE_FOLDER：您存储剧集封面图片的文件夹路径。（每次只能为单季添加封面图片，每集只能上传一张图片，图片请按集编号命名，文件夹内请只包含单季的图片）
   - LANGUAGE：您添加的封面图片的语言代码。（请以您设置的语言偏好为依据进行设置，例如：界面语言为 `汉语` 时，`汉语` 表示汉语，`英语` 表示英语；界面语言为 `English` 时，`Chinese` 表示汉语，`English` 表示英语。）
3. 修改 `start.command` 中的路径，以指向您存放 `auto-add-covers.py` 脚本的目录。
4. 双击运行 `start.command` 脚本以执行 `auto-add-covers.py` 脚本。
5. 脚本会自动打开新的 Chrome 浏览器窗口，自动登录到 TMDB 网站，并根据提供的剧集封面图片上传图片。脚本会按照数字从小到大的顺序上传提供的封面图片，如果上传失败，脚本将显示相应的提示信息，并继续处理下一个图片。当所有图片都处理完成后，脚本将显示成功上传的封面数和失败的封面数（如果有）。

### 注意事项
- 请确保您拥有合法的 TMDB 帐户，并且具有足够的权限执行所需的操作。
- 使用脚本时，请确保您的网络连接正常，并且 TMDB 网站可以正常访问。
- 请确保设置的 `LANGUAGE` 与您提供的封面图片语言一致。
- 请确保 TMDB 的界面语言与您设置 `LANGUAGE` 时使用的语言匹配，即界面语言为 `汉语` 时请使用 `汉语` 描述语言，界面语言为 `英语` 时请使用 `英语` 描述语言。
- 请确保提供的剧集封面图片是按集编号命名的，并以 `.jpg` 作为文件扩展名。
- 请确保脚本运行时输入法的语言为英语，且用到的文件夹或文件路径及名称中不要包含中文和特殊符号。
- 使用脚本时，请关闭所有使用 `Shift` 键为快捷键的应用程序，或将快捷键设置为其他键，以免运行时触发其他任务，影响脚本正常运行。
- 使用脚本时，请勿对屏幕进行任何操作，以免中断脚本运行。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。
