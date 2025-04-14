# TMDB Automation <a name="tmdb-automation-zh"></a>
<a href="#tmdb-automation-en">Switch to English</a>

使用 TMDB Automation 可以利用 selenium 通过网页自动化实现自动向 TMDB 添加剧集信息和图片。由于 TMDB 不支持通过 API 向网站添加内容，所以我选择了使用 selenium 来实现这个功能。TMDB Automation 共包含三个工具，Auto Add Episodes 可以用来添加剧集信息，Auto Add Backdrops 可以用来添加剧照图片，Auto Update Episodes 可以用来更新（修改）剧集信息。
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
- 使用脚本时，请确保你的网络连接正常，并且 TMDB 网站可以正常访问。
- 请确保你的 TMDB 帐户拥有足够的权限执行相关操作。
- 请确保设置的 `LANGUAGE_CODE` 与你提供的剧集信息的语言一致。
- 请确保 TMDB 账户的「语言偏好设置」中的「网站界面的默认语言」与你设置的 `LANGUAGE_CODE` 一致。
- 请确保你按照要求整理了剧集信息。不同语言对 `播出日期` 的格式要求可能不同，当语言为 `汉语` 时日期格式为 `YYYY/MM/DD` 如 `2025/1/20`，当语言为 `英语` 时日期格式为 `MM/DD/YYYY` 如 `1/20/2025`，请根据你的语言使用对应的格式，或者使用 `YYYY-MM-DD` 格式 如 `2025-1-20`。
- 若提供的剧集信息中包含已经存在于 TMDB 上的剧集，脚本将跳过这些剧集并在控制台显示相应的提示信息，然后继续添加其他剧集。
- 脚本将自动从 `/auto-add-episodes/episodes.txt` 文件内删除已成功添加的剧集信息，建议运行脚本前先做好备份。
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
- 使用脚本时，请确保你的网络连接正常，并且 TMDB 网站可以正常访问。
- 请确保你的 TMDB 帐户拥有足够的权限执行相关操作。
- 请确保设置的 `LANGUAGE` 与你提供的剧集图片的语言一致，若图片上没有文字，请设置为 `No Language`。
- 请确保 TMDB 账户的「语言偏好设置」中的「网站界面的默认语言」与你设置的 `LANGUAGE` 一致。
- 请确保你按照要求整理了剧集图片。请将剧集图片保存为 `jpg` 或 `jpeg` 格式，其他格式可能不受支持。请将剧集图片裁剪为 `16:9` 的比例，其他比例可能不受支持。
- 无论剧集图片对应的剧集是否已经存在剧集图片，脚本始终都会上传你提供的图片。
- 脚本将自动从 `/auto-add-backdrops/backdrops` 文件夹内删除已成功添加的剧集图片，建议运行脚本前先做好备份。
- 脚本运行时，请勿操作键盘和鼠标，以免引发错误。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。
<br>

## auto-update-episodes
### 运行条件
- 操作系统为 Windows、MacOS 或 Linux。
- 安装了 Python 3.0 或更高版本。
- 安装了必要的第三方库：selenium。（可以通过 `pip3 install selenium` 安装）
- 安装了 Chrome 浏览器和对应版本的 [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads)。
- 有可用的 TMDB 账号。

### 使用方法
1. 将仓库克隆或下载到计算机上的一个目录中。
2. 根据需要，修改脚本中的参数：`TMDB_USERNAME`、`TMDB_PASSWORD`、`EPISODES_URL`、`DATA_FILE` 和 `LANGUAGE_CODE`。
   - TMDB_USERNAME：您的 TMDB 用户名。
   - TMDB_PASSWORD：您的 TMDB 用户密码。
   - EPISODES_URL：您要更新剧集的网址。（例如：`https://www.themoviedb.org/tv/201900/season/1/episode/1/edit?active_nav_item=primary_facts`，需要是具体某一季的集的编辑页面的完整地址）
   - DATA_FILE：您存储剧集信息的文本文件路径。（文本每一行代表一集的信息，需要包含五个由 `;` 分隔的字段，分别表示集编号、播出日期、时长、名字和分集剧情。例如：`336;2023/6/29;47;滑到他們的影片就停不下來！超可愛網紅小朋友們來啦！;小孩就是流量密碼？只要有小孩的影片流量就會高嗎？！今天製作單位就找來幾位「小朋友網紅」到現場，要看看他們到底是有什麼魔力能讓人如此著迷！`）
   - LANGUAGE_CODE：您更新内容的语言代码。（例如：`zh_CN` 表示汉语，`en_US` 表示英语，以 TMDB 编辑页面显示的语言代码为准，注意需要将 `-` 改为 `_`。）
3. 修改 `start.command (Mac)` 或 `start.bat (Win)` 中的路径，以指向您存放 `auto-update-episodes.py` 脚本的目录。
4. 双击运行 `start.command` 或 `start.bat` 脚本以执行 `auto-update-episodes.py` 脚本。
5. 脚本会自动打开新的 Chrome 浏览器窗口，自动登录到 TMDB 网站，并根据提供的剧集信息更新每一集的信息。当所有剧集信息都处理完成后，脚本将显示成功更新的剧集数和失败的剧集数（如果有）。

### 注意事项
- 请确保您拥有合法的 TMDB 帐户，并且具有足够的权限执行所需的操作。
- 使用脚本时，请确保您的网络连接正常，并且 TMDB 网站可以正常访问。
- 请确保设置的 `LANGUAGE_CODE` 与您提供的剧集信息的文本语言一致。
- 请确保 TMDB 账户的语言偏好设置与您设置的 `LANGUAGE_CODE` 一致。
- 使用脚本时，请遵守 TMDB 网站的使用条款和规定，以确保合法合规。
<br>
<br>

# tmdb-automation
tmdb-automation is a tool that automates the process of adding TV show episodes and cover images to TMDB using Selenium web automation. Since TMDB does not support adding content to the site via API, I chose to use selenium to achieve this functionality. tmdb-automation contains three scripts: auto-add-episodes for adding episodes, auto-add-covers for adding episode covers, and auto-update-episodes for updating (modifying) episode information.
<br>
<br>
## auto-add-episodes
### Requirements
- Operating system: Windows, MacOS, or Linux.
- Installed Python 3.0 or higher.
- Installed required third-party library: selenium. (Install with `pip3 install selenium`)
- Installed Chrome browser and corresponding version of [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads).
- A valid TMDB account.

### Usage
1. Clone or download the repository to a directory on your computer.
2. Modify the parameters in the script as needed: `TMDB_USERNAME`, `TMDB_PASSWORD`, `EPISODES_URL`, `DATA_FILE` and `LANGUAGE_CODE`.
   - TMDB_USERNAME: Your TMDB username.
   - TMDB_PASSWORD: Your TMDB password.
   - EPISODES_URL: The URL of the TV show episodes editing page you want to add episodes to. (e.g., `https://www.themoviedb.org/tv/229116-dust/season/8/edit?active_nav_item=episodes`, needs to be the full address of the edit page for a specific season of episodes)
   - DATA_FILE: The path to the text file where you store episode information. (Each line of text represents one episode’s information, containing five fields separated by `;`, representing episode number, air date, duration, name and episode overview. For example: `53;6/28/2023;19;Fearfully Made;Sundered from his wife, Arthur's care falls to a machine.`）
   - LANGUAGE_CODE: The language code for the content you are adding. (e.g., `zh-CN` for Chinese, `en-US` for English, based on the language code displayed on the TMDB edit page)
3. Modify the path in `start.command (Mac)` or `start.bat (Win)` to point to the directory where you store the `auto-add-episodes.py` script.
4. Double-click `start.command` or `start.bat` to execute the `auto-add-episodes.py` script.
5. The script will automatically open a new Chrome browser window, log in to the TMDB website automatically, and add new episodes based on the provided episode information. If there are episodes in the provided episode information that already exist on TMDB, the script will skip these episodes and display corresponding prompt information, then continue adding other episodes. When all episode information has been processed, the script will display the number of successfully added episodes and failed episodes (if any).

### Notes
- Ensure that you have a valid TMDB account and sufficient permissions to perform the required actions.
- Make sure you have a stable internet connection and can access the TMDB website.
- Ensure that the `LANGUAGE_CODE` matches the language used in the provided episode information.
- Set your TMDB account language preferences to match the `LANGUAGE_CODE`.
- Ensure that the format of the provided episode information file matches the format specified in the script. The date format may vary depending on the language. For example, for `Chinese`, the date format is `YYYY/MM/DD` (e.g., `2023/1/20`), and for `English`, the date format is `MM/DD/YYYY` (e.g., `1/20/2023`). Please use the appropriate format based on your language.
- Follow the terms of use and regulations of the TMDB website while using the script.
<br>

## auto-add-covers
### Requirements
- Operating system: MacOS.
- Installed Python 3.0 or higher.
- Installed required third-party library: selenium. (Install with `pip3 install selenium`)
- Installed Chrome browser and corresponding version of [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads).
- A valid TMDB account.

### Usage
1. Clone or download the repository to a directory on your computer.
2. Modify the parameters in the script as needed: `TMDB_USERNAME`, `TMDB_PASSWORD`, `EPISODES_URL`, `IMAGE_FOLDER` and `LANGUAGE`.
   - TMDB_USERNAME: Your TMDB username.
   - TMDB_PASSWORD: Your TMDB password.
   - EPISODE_URL: The URL of the TV show episode's backdrop images page you want to add cover images to. (e.g., `https://www.themoviedb.org/tv/229116-dust/season/0/episode/1/images/backdrops`. It should be the URL of a specific episode's backdrop images page)
   - IMAGE_FOLDER: The path to the folder where you store episode cover images. (Only one season of cover images can be added at a time, only one image can be uploaded per episode, images should be named by episode number, and only images from a single season should be included in the folder)
   - LANGUAGE: The language of the cover images you are adding (Please set according to your language preference, For example, when the interface language is `汉语`, `汉语` means Chinese, `英语` means English; when the interface language is `English`, `Chinese` means Chinese, `English` means English.)
3. Modify the path in `start.command (Mac)` or `start.bat (Win)` to point to the directory where you store the `auto-add-covers.py` script.
4. Double-click `start.command` or `start.bat` to execute the `auto-add-covers.py` script.
5. The script will automatically open a new Chrome browser window, log in to the TMDB website automatically, and upload cover images based on the provided episode cover images. The script will upload the provided cover images in ascending numerical order, if uploading fails, the script will display corresponding prompt information and continue processing the next image. When all images have been processed, the script will display the number of successfully uploaded covers and failed covers (if any).

### Notes
- Ensure that you have a valid TMDB account and sufficient permissions to perform the required actions.
- Make sure you have a stable internet connection and can access the TMDB website.
- Ensure that the `LANGUAGE` matches the language used for the provided cover images.
- Ensure that when setting `LANGUAGE`, you use a language that matches your TMDB interface language.
- Ensure that your provided episode cover images are named by episode number and have `.jpg` as their file extension.
- Please ensure that the input method language is set to English while running the script, and the folder names, file names, and directory paths used should only contain English characters. They should not include characters from other languages or special characters.
- When using the script, please close any applications that have assigned shortcuts using the `Shift` key or change their shortcuts to use other keys. This will prevent the possibility of triggering unintended processes during script execution, which could potentially interfere with the script's operation.
- While running the script, please refrain from performing any actions on the screen to avoid interrupting the script's execution.
- Follow the terms of use and regulations of the TMDB website while using the script.
<br>

## auto-update-episodes
### Requirements
- Operating system: Windows, MacOS, or Linux.
- Installed Python 3.0 or higher.
- Installed required third-party library: selenium. (Install with `pip3 install selenium`)
- Installed Chrome browser and corresponding version of [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads).
- A valid TMDB account.

### Usage
1. Clone or download the repository to a directory on your computer.
2. Modify the parameters in the script as needed: `TMDB_USERNAME`, `TMDB_PASSWORD`, `EPISODES_URL`, `DATA_FILE`, and `LANGUAGE_CODE`.
   - TMDB_USERNAME: Your TMDB username.
   - TMDB_PASSWORD: Your TMDB password.
   - EPISODES_URL: The URL of the episode's edit page you want to update. (e.g., `https://www.themoviedb.org/tv/201900/season/1/episode/1/edit?active_nav_item=primary_facts`, needs to be the full address of the edit page of a specific season’s episode)
   - DATA_FILE: The path to the text file where you store episode information. (Each line of text represents one episode’s information, containing five fields separated by `;`, representing episode number, air date, duration, name and episode overview. For example: `53;6/28/2023;19;Fearfully Made;Sundered from his wife, Arthur's care falls to a machine.`）
   - LANGUAGE_CODE: The language code for the content you are adding. (e.g., `zh_CN` for Chinese, `en_US` for English, based on the language code displayed on the TMDB edit page, note that you need to change `-` to `_`.)
3. Modify the path in `start.command (Mac)` or `start.bat (Win)` to point to the directory where you store the `auto-update-episodes.py` script.
4. Double-click `start.command` or `start.bat` to execute the `auto-update-episodes.py` script.
5. The script will automatically open a new Chrome browser window, log in to the TMDB website automatically, and update each episode according to the provided episode information. When all episode information has been processed, the script will display the number of episodes successfully updated and the number of failed episodes (if any).

### Notes
- Ensure that you have a valid TMDB account and sufficient permissions to perform the required actions.
- Make sure you have a stable internet connection and can access the TMDB website.
- Ensure that the `LANGUAGE_CODE` matches the language used in the provided episode information.
- Set your TMDB account language preferences to match the `LANGUAGE_CODE`.
- Follow the terms of use and regulations of the TMDB website while using the script.
