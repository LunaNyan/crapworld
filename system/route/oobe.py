from system.engine.server import app
from system.tool.renderer import load_html_shard, render_mainpage, fill_args


def render_list(current=None):
    cms_lst = [
        ["시작", "1"],
        ["계정 만들기", "2"],
        ["완료", "9"]
    ]
    html_delimiter = load_html_shard("diary/delimiter")
    html_delimiter_end = load_html_shard("diary/delimiter_end")
    html_list_item = load_html_shard("admin/content_list_item")
    html_list_item_cur = load_html_shard("admin/content_list_item_selected")
    ht = ""

    ht += html_delimiter_end
    ht += html_delimiter.replace("{group_title}", f"시작하기")
    for i in cms_lst:
        if i[1] == current:
            ht2 = html_list_item_cur.replace('{title}', i[0])
        else:
            ht2 = html_list_item.replace('<a href="/admin/content/{cms}">{title}</a>', i[0])
        ht += ht2
    ht += html_delimiter_end
    return ht


@app.route('/oobe/account_generation')
def oobe_account_generation():
    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('oobe/account_generation')

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("2")
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary", oobe=True)


@app.route('/oobe')
def oobe_start():
    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('oobe/welcome')

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("1")
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary", oobe=True)
