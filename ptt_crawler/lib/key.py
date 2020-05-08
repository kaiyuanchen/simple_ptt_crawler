class CommandKey(object):
    Yes = "N\r\n"
    No = "N\r\n"
    Enter = "\r\n"

    Up = '\x1b[A'
    Down = '\x1b[B'
    Right = '\x1b[C'
    Left = '\x1b[D'

    PrevPage = "\x1b[5~"
    NextPage = "\x1b[6~"
    End = "\x1b[F"


class ScreenKeyword(object):
    logins = [
        "任意鍵",
        "登入中，請稍候...",
        "您想刪除其他重複登入的連線嗎",
        "正在更新與同步線上使用者及好友名單",
        "請按任意鍵繼續"
    ]

    login_multi = "您想刪除其他重複登入的連線嗎"

    login_error = "您要刪除以上錯誤嘗試的記錄嗎"

    any = "請按任意鍵繼續"

    menu = "主功能表"

    animation = "這份文件是可播放的文字動畫，要開始播放嗎"

    article_position = [
        r"瀏覽\s第\s([0-9\/]+)",
        r"\s+頁\s+",
        r"\(\s*([0-9]+)\%\)",
        r"\s+",
        r"目前顯示:\s第\s([0-9]+)\~([0-9]+)"
    ]
