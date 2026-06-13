from pathlib import Path
import sys
import time
import tkinter as tk

from PIL import Image, ImageTk

from util import lead_distance, win_lose, you, zhang


APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
RESOURCE_DIR = APP_DIR / "resources"
FONT = ("Microsoft YaHei UI", 20)
WIDTH = 639
HEIGHT = 585
SHOP_HEIGHT = 629


class RunZhangGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("跑赢张雪峰")
        self.root.resizable(False, False)

        # 设置页面参数
        self.canvas = tk.Canvas(
            self.root, width=WIDTH, height=HEIGHT, highlightthickness=0
        )
        self.canvas.pack()

        self.images = {}
        self.page = "title"
        self.game_running = False
        self.last_tick = time.perf_counter()
        self.result_message = ""
        self.load_images()
        self.canvas.bind("<Button-1>", self.on_click)
        self.show_title()

    # 加载文件中包含的各个页面图片
    def load_images(self):
        for name in (
            "title",
            "rules",
            "shop",
            "runway_main",
            "runway_nether",
            "win_main",
            "win_nether",
            "lose_main",
            "lose_nether",
        ):
            image = Image.open(RESOURCE_DIR / f"{name}.png")
            self.images[name] = ImageTk.PhotoImage(image)

    def set_size(self, height=HEIGHT):
        self.canvas.config(width=WIDTH, height=height)
        self.root.geometry(f"{WIDTH}x{height}")

    # 清空画布
    def clear(self):
        self.canvas.delete("all")

    # 先清空原来的背景，再转到新的背景
    def set_background(self, name):
        self.clear()
        self.canvas.create_image(0, 0, anchor="nw", image=self.images[name])

    # 标题页面
    def show_title(self):
        self.page = "title"
        self.game_running = False
        self.set_size()
        self.set_background("title")

    # 规则页面
    def show_rules(self):
        self.page = "rules"
        self.set_size()
        self.set_background("rules")

    # 商店页面
    def show_shop(self):
        self.page = "shop"
        self.set_size(SHOP_HEIGHT)
        self.set_background("shop")
        self.draw_shop_status()

    # 更新道具购买状态
    def draw_shop_status(self):
        if you.chocliz:
            self.canvas.create_text(100, 74, text="已食用", font=FONT, fill="black")
        if you.sprite:
            self.canvas.create_text(324, 74, text="已服用", font=FONT, fill="black")
        if zhang.portal:
            self.canvas.create_text(537, 74, text="已激活", font=FONT, fill="black")

    # 开始游戏，设定初始参数
    def start_game(self):
        self.page = "game"
        self.set_size()
        you.distance = 0
        you.velocity = 1
        zhang.distance = 0
        zhang.velocity = 8
        zhang.shift_velocity()
        self.game_running = True
        self.last_tick = time.perf_counter()
        self.render_game()
        self.tick()

    def render_game(self):
        background = "runway_nether" if zhang.portal else "runway_main"
        self.set_background(background)
        self.canvas.create_text(
            360,
            523,
            text=str(lead_distance()),
            font=("Microsoft YaHei UI", 14),
            fill="black",
        )

        zhang_x = self.runner_x(zhang.distance)
        you_x = self.runner_x(you.distance)
        self.canvas.create_oval(zhang_x, 250, zhang_x + 64, 314, width=4)
        self.canvas.create_text(zhang_x + 32, 282, text="张", font=FONT, fill="black")
        self.canvas.create_oval(you_x, 372, you_x + 64, 436, width=4)
        self.canvas.create_text(you_x + 32, 404, text="你", font=FONT, fill="black")

    def runner_x(self, distance):
        return max(34, min(541, 34 + int(distance / 20) % 508))

    def tick(self):
        if not self.game_running:
            return

        now = time.perf_counter()
        elapsed_ms = max(1, int((now - self.last_tick) * 1000))
        self.last_tick = now
        zhang.distance += zhang.velocity * elapsed_ms / 40

        result, message = win_lose()
        if result is not None:
            self.end_game(result, message)
            return

        self.render_game()
        self.root.after(20, self.tick)

    # 结束游戏
    def end_game(self, won, message):
        self.game_running = False
        self.page = "result"
        self.result_message = message

        if won:
            background = "win_nether" if zhang.portal else "win_main"
        else:
            background = "lose_nether" if zhang.portal else "lose_main"
        self.set_background(background)
        self.canvas.create_text(
            WIDTH // 2,
            260,
            text=message,
            font=("Microsoft YaHei UI", 18),
            fill="black",
            width=280,
        )

        you.reset()
        zhang.reset()

    # 点击鼠标时的反应
    def on_click(self, event):
        x, y = event.x, event.y
        # 标题页面，点击对应按钮跳转对应页面
        if self.page == "title":
            if self.in_rect(x, y, 56, 439, 168, 497):
                self.start_game()
            elif self.in_rect(x, y, 254, 443, 356, 498):
                self.show_rules()
            elif self.in_rect(x, y, 456, 443, 567, 502):
                self.show_shop()
        # 规则页面，点击返回按钮返回标题页面
        elif self.page == "rules":
            if self.in_rect(x, y, 217, 428, 438, 503):
                self.show_title()
        # 商店页面，点击对应按钮购买物品，点击其他位置返回标题页面
        elif self.page == "shop":
            if self.in_rect(x, y, 13, 438, 190, 533):
                you.purchase_chocliz()
                self.show_shop()
            elif self.in_rect(x, y, 233, 438, 411, 533):
                you.purchase_sprite()
                self.show_shop()
            elif self.in_rect(x, y, 447, 438, 626, 533):
                zhang.portal = True
                self.show_shop()
            elif self.in_rect(x, y, 190, 560, 439, 620) or y >= 540:
                self.show_title()
        # 游戏页面，点击时控制角色跑动
        elif self.page == "game":
            you.chase()
            result, message = win_lose()
            if result is not None:
                self.end_game(result, message)
            else:
                self.render_game()
        # 结算页面，点击返回标题
        elif self.page == "result":
            time.sleep(5)
            self.show_title()

    @staticmethod
    def in_rect(x, y, left, top, right, bottom):
        return left <= x <= right and top <= y <= bottom

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    RunZhangGame().run()
