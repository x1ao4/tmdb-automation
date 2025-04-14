# TMDB Automation <a name="tmdb-automation-zh"></a>
<a href="#tmdb-automation-en">Switch to English</a>

使用 TMDB Automation 可以利用 selenium 通过网页自动化实现自动向 [TMDB](https://www.themoviedb.org/) 添加剧集信息和图片。由于 TMDB 不支持通过 API 向网站添加内容，所以我选择了使用 selenium 来实现这个功能。TMDB Automation 共包含三个工具，Auto Add Episodes 可以用来添加剧集信息，Auto Add Backdrops 可以用来添加剧集图片（剧照），Auto Update Episodes 可以用来更新（修改）剧集信息。
<br>
<br>
## Auto Add Episodes
### 运行条件
- 安装了 Python 3.9 或更高版本。
- 使用命令 `pip3 install -r requirements.txt` 安装了必要的第三方库。
- 安装了 Chrome 浏览器和对应版本的 [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads)。
- 有可用的 TMDB 账号。
- 按要求整理好了需要添加的剧集信息。

### 配置说明
在使用 Auto Add Episodes 前，请先参考以下提示（示例）对 `/auto-add-episodes/config.ini` 进行配置。
```
[TMDB]
# 你的 TMDB 用户名
USERNAME = YOUR_TMDB_USERNAME
# 你的 TMDB 用户密码
PASSWORD = YOUR_TMDB_PASSWORD

[SHOW]
# 你要添加的电视节目的剧集所属季的编辑页面的集数编辑页面的网址，如下方示例
EPISODES_URL = https://www.themoviedb.org/tv/42009-black-mirror/season/1/edit?active_nav_item=episodes
# 你要添加的剧集信息的语言，如 zh-CN 表示汉语，en-US 表示英语，以 TMDB 使用的语言代码为准
LANGUAGE_CODE = zh-CN
```

请将要添加的剧集信息按照 `集编号;播出日期;时长;名字;分集剧情` 的顺序整理（每行代表一集）并保存为 `/auto-add-episodes/episodes.txt`。
```
1;2011/12/4;45;国歌;备受爱戴的苏珊娜公主遭人绑架，这让首相麦克尔·凯罗陷入了可怕的两难境地。
2;2011/12/11;62;一千五百万点;一位女士未能在歌唱比赛中受到评委的青睐，她必须做出选择，进行有辱人格的表演还是回到奴隶般的生活状态。
3;2011/12/18;50;你的人生;在不久的将来，每个人都可以使用一种记忆植入装置，了解人类做过、看过和听过的所有事情。
```

### 使用方法
1. 通过 [Releases](https://github.com/x1ao4/tmdb-automation/releases) 下载最新版本的压缩包并解压到本地目录中。
2. 用记事本或文本编辑打开目录中的 `/auto-add-episodes/config.ini` 文件，填写你的 TMDB 用户名（`USERNAME`）、用户密码（`PASSWORD`）以及你要添加的剧集的相关信息。
3. 将整理好的剧集信息按要求保存在 `/auto-add-episodes/episodes.txt` 文件内。
4. 双击 `aae.bat`（Windows）或 `aae.command`（Mac）即可启动 Auto Add Episodes。
5. 脚本会自动打开新的 Chrome 浏览器窗口，自动登录到 TMDB 网站，根据提供的剧集信息自动添加新的剧集，并在控制台显示处理结果。在所有剧集信息都处理完成后，打开的 Chrome 浏览器窗口将自动关闭，控制台会显示统计信息然后结束运行。

### 注意事项
- 请确保你的网络可以正常访问 TMDB 的网站。
- 请确保你的 TMDB 帐户拥有足够的权限执行相关操作。
- 请确保设置的 `LANGUAGE_CODE` 与你提供的剧集信息的语言一致。
- 请确保 TMDB 账户的「语言偏好设置」中的「网站界面的默认语言」与你设置的 `LANGUAGE_CODE` 一致。
- 请确保你按照要求整理了剧集信息。不同语言对 `播出日期` 的格式要求可能不同，当语言为 `汉语` 时日期格式为 `YYYY/MM/DD` 如 `2025/1/20`，当语言为 `英语` 时日期格式为 `MM/DD/YYYY` 如 `1/20/2025`，请根据你的语言使用对应的格式，或者使用 `YYYY-MM-DD` 格式 如 `2025-1-20`。
- 若提供的剧集信息中包含已经存在于 TMDB 上的剧集，脚本将跳过这些剧集并在控制台显示相应的提示信息，然后继续添加其他剧集。
- 脚本将自动从 `/auto-add-episodes/episodes.txt` 文件中删除已成功添加的剧集信息，建议运行脚本前先做好备份。
- 脚本运行时，请勿操作键盘和鼠标，以免引发错误。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。
<br>

## Auto Add Backdrops
### 运行条件
- 安装了 Python 3.9 或更高版本。
- 使用命令 `pip3 install -r requirements.txt` 安装了必要的第三方库。
- 安装了 Chrome 浏览器和对应版本的 [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads)。
- 有可用的 TMDB 账号。
- 按要求整理好了需要添加的剧集图片（剧照）。

### 配置说明
在使用 Auto Add Backdrops 前，请先参考以下提示（示例）对 `/auto-add-backdrops/config.ini` 进行配置。
```
[TMDB]
# 你的 TMDB 用户名
USERNAME = YOUR_TMDB_USERNAME
# 你的 TMDB 用户密码
PASSWORD = YOUR_TMDB_PASSWORD

[SHOW]
# 你要添加的电视节目的剧集图片（剧照）所属季的任意一集的剧照页面的网址，如下方示例
EPISODE_URL = https://www.themoviedb.org/tv/42009-black-mirror/season/1/episode/1/images/backdrops
# 你要添加的剧集图片的语言，根据你的 TMDB 账户的语言偏好进行设置，如网站界面的默认语言为 `汉语` 时，`汉语` 表示汉语，`英语` 表示英语；默认语言为 `English` 时，`Chinese` 表示汉语，`English` 表示英语
LANGUAGE = 汉语
```

请使用 `集编号` 为你要添加的剧集图片（剧照）命名（如 `1.jpg`、`2.jpg` 和 `3.jpg` 分别代表第一集、第二集和第三集的剧照），并保存在 `/auto-add-backdrops/backdrops` 文件夹内。

### 使用方法
1. 通过 [Releases](https://github.com/x1ao4/tmdb-automation/releases) 下载最新版本的压缩包并解压到本地目录中。
2. 用记事本或文本编辑打开目录中的 `/auto-add-backdrops/config.ini` 文件，填写你的 TMDB 用户名（`USERNAME`）、用户密码（`PASSWORD`）以及你要添加的剧集图片的相关信息。
3. 将整理好的剧集图片按要求保存在 `/auto-add-backdrops/backdrops` 文件夹内。
4. 双击 `aab.bat`（Windows）或 `aab.command`（Mac）即可启动 Auto Add Backdrops。
5. 脚本会自动打开新的 Chrome 浏览器窗口，自动登录到 TMDB 网站，根据提供的剧集图片自动为对应的剧集上传图片，并在控制台显示处理结果。在所有剧集图片都处理完成后，打开的 Chrome 浏览器窗口将自动关闭，控制台会显示统计信息然后结束运行。

### 注意事项
- 请确保你的网络可以正常访问 TMDB 的网站。
- 请确保你的 TMDB 帐户拥有足够的权限执行相关操作。
- 请确保设置的 `LANGUAGE` 与你提供的剧集图片的语言一致，若图片上没有文字，请设置为 `No Language`。
- 请确保 TMDB 账户的「语言偏好设置」中的「网站界面的默认语言」与你设置的 `LANGUAGE` 一致（`No Language` 除外）。
- 请确保你按照要求整理了剧集图片。请将剧集图片保存为 `jpg` 或 `jpeg` 格式，其他格式可能不受支持。请将剧集图片裁剪为 `16:9` 的比例，其他比例可能不受支持。
- 无论剧集图片对应的剧集是否已经存在剧集图片，脚本始终都会上传你提供的图片。
- 脚本将自动从 `/auto-add-backdrops/backdrops` 文件夹中删除已成功添加的剧集图片，建议运行脚本前先做好备份。
- 脚本运行时，请勿操作键盘和鼠标，以免引发错误。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。
<br>

## Auto Update Episodes
### 运行条件
- 安装了 Python 3.9 或更高版本。
- 使用命令 `pip3 install -r requirements.txt` 安装了必要的第三方库。
- 安装了 Chrome 浏览器和对应版本的 [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads)。
- 有可用的 TMDB 账号。
- 按要求整理好了需要更新（修改）的剧集信息。

### 配置说明
在使用 Auto Update Episodes 前，请先参考以下提示（示例）对 `/auto-update-episodes/config.ini` 进行配置。
```
[TMDB]
# 你的 TMDB 用户名
USERNAME = YOUR_TMDB_USERNAME
# 你的 TMDB 用户密码
PASSWORD = YOUR_TMDB_PASSWORD

[SHOW]
# 你要更新（修改）的电视节目的剧集所属季的任意一集的编辑页面的网址，如下方示例
EPISODE_URL = https://www.themoviedb.org/tv/42009-black-mirror/season/1/episode/1/edit?active_nav_item=primary_facts
# 你要更新的剧集信息的语言，如 zh_CN 表示汉语，en_US 表示英语，以 TMDB 使用的语言代码为准，并将 - 改为 _
LANGUAGE_CODE = zh_CN
```

请将要更新的剧集信息按照 `集编号;播出日期;时长;名字;分集剧情` 的顺序整理（每行代表一集）并保存为 `/auto-update-episodes/episodes.txt`。
```
1;2011/12/4;45;国歌;备受爱戴的苏珊娜公主遭人绑架，这让首相麦克尔·凯罗陷入了可怕的两难境地。
2;2011/12/11;62;一千五百万点;一位女士未能在歌唱比赛中受到评委的青睐，她必须做出选择，进行有辱人格的表演还是回到奴隶般的生活状态。
3;2011/12/18;50;你的人生;在不久的将来，每个人都可以使用一种记忆植入装置，了解人类做过、看过和听过的所有事情。
```

### 使用方法
1. 通过 [Releases](https://github.com/x1ao4/tmdb-automation/releases) 下载最新版本的压缩包并解压到本地目录中。
2. 用记事本或文本编辑打开目录中的 `/auto-update-episodes/config.ini` 文件，填写你的 TMDB 用户名（`USERNAME`）、用户密码（`PASSWORD`）以及你要更新的剧集的相关信息。
3. 将整理好的剧集信息按要求保存在 `/auto-update-episodes/episodes.txt` 文件内。
4. 双击 `aue.bat`（Windows）或 `aue.command`（Mac）即可启动 Auto Update Episodes。
5. 脚本会自动打开新的 Chrome 浏览器窗口，自动登录到 TMDB 网站，根据提供的剧集信息自动更新（覆盖）剧集信息，并在控制台显示处理结果。在所有剧集信息都处理完成后，打开的 Chrome 浏览器窗口将自动关闭，控制台会显示统计信息然后结束运行。

### 注意事项
- 请确保你的网络可以正常访问 TMDB 的网站。
- 请确保你的 TMDB 帐户拥有足够的权限执行相关操作。
- 请确保设置的 `LANGUAGE_CODE` 与你提供的剧集信息的语言一致。
- 请确保 TMDB 账户的「语言偏好设置」中的「网站界面的默认语言」与你设置的 `LANGUAGE_CODE` 一致。
- 请确保你按照要求整理了剧集信息。不同语言对 `播出日期` 的格式要求可能不同，当语言为 `汉语` 时日期格式为 `YYYY/MM/DD` 如 `2025/1/20`，当语言为 `英语` 时日期格式为 `MM/DD/YYYY` 如 `1/20/2025`，请根据你的语言使用对应的格式，或者使用 `YYYY-MM-DD` 格式 如 `2025-1-20`。
- 脚本仅支持更新 TMDB 上已存在的剧集的信息。
- 脚本将自动从 `/auto-update-episodes/episodes.txt` 文件中删除已成功更新的剧集信息，建议运行脚本前先做好备份。
- 脚本运行时，请勿操作键盘和鼠标，以免引发错误。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。

## 赞赏
如果你觉得这个项目对你有用，可以考虑请我喝杯咖啡或者给我一个⭐️。谢谢你的支持！

<img width="383" alt="赞赏" src="https://github.com/user-attachments/assets/bdd2226b-6282-439d-be92-5311b6e9d29c">
<br><br>
<a href="#tmdb-automation-zh">回到顶部</a>
<br>
<br>
<br>

# TMDB Automation <a name="tmdb-automation-en"></a>
<a href="#tmdb-automation-zh">切换至中文</a>

tmdb-automation is a tool that automates the process of adding TV show episodes and cover images to TMDB using Selenium web automation. Since TMDB does not support adding content to the site via API, I chose to use selenium to achieve this functionality. tmdb-automation contains three scripts: auto-add-episodes for adding episodes, auto-add-covers for adding episode covers, and auto-update-episodes for updating (modifying) episode information.
<br>
<br>

## Support
If you found this helpful, consider buying me a coffee or giving it a ⭐️. Thanks for your support!

<img width="383" alt="Support" src="https://github.com/user-attachments/assets/bdd2226b-6282-439d-be92-5311b6e9d29c">
<br><br>
<a href="#tmdb-automation-zh">Back to Top</a>
