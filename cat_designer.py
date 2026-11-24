import random
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox


class CatDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("고양이 모양 만들기")
        self.root.geometry("980x650")
        self.root.configure(bg="#f4f1ea")

        self.fur = "#FFFDF8"
        self.eye = "#3A211C"
        self.pupil = "#21100D"
        self.nose = "#3A211C"
        self.inner_ear = "#F5A4A1"

        self.ear_size = tk.IntVar(value=64)
        self.eye_size = tk.IntVar(value=43)
        self.face_width = tk.IntVar(value=378)
        self.face_height = tk.IntVar(value=289)
        self.pupil_shape = tk.StringVar(value="둥근")
        self.expression = tk.StringVar(value="행복")
        self.pattern = tk.StringVar(value="단색")

        self.create_layout()
        self.pupil_shape.trace_add("write", self.draw_cat)
        self.expression.trace_add("write", self.draw_cat)
        self.pattern.trace_add("write", self.draw_cat)
        self.draw_cat()

    def create_layout(self):
        controls = tk.Frame(self.root, width=310, bg="#fffdf8", padx=18, pady=16)
        controls.pack(side="left", fill="y")
        controls.pack_propagate(False)

        tk.Label(
            controls,
            text="고양이 꾸미기",
            font=("Noto Sans KR", 18, "bold"),
            bg="#fffdf8",
            fg="#2e2a25",
        ).pack(pady=(0, 12))

        self.add_color_button(controls, "털 색깔", "fur")
        self.add_color_button(controls, "눈동자 색깔", "eye")
        self.add_color_button(controls, "동공 색깔", "pupil")
        self.add_color_button(controls, "코 색깔", "nose")

        tk.Label(
            controls,
            text="고정 크기",
            anchor="w",
            bg="#fffdf8",
            font=("Noto Sans KR", 10, "bold"),
        ).pack(fill="x", pady=(8, 2))
        tk.Label(
            controls,
            text="귀 64  ·  눈 43  ·  얼굴 378 × 289",
            anchor="w",
            bg="#fffdf8",
            fg="#665f57",
            font=("Noto Sans KR", 9),
        ).pack(fill="x", pady=(0, 5))

        self.add_option(controls, "동공 모양", self.pupil_shape,
                        ["세로", "둥근", "작은 점"])
        self.add_option(controls, "표정", self.expression,
                        ["행복", "차분", "신비", "졸림"])
        self.add_option(controls, "무늬", self.pattern,
                        ["단색", "줄무늬", "점무늬", "삼색"])

        buttons = tk.Frame(controls, bg="#fffdf8")
        buttons.pack(fill="x", pady=(16, 0))
        tk.Button(
            buttons, text="랜덤 고양이", command=self.randomize,
            bg="#5C9EAD", fg="white", relief="flat", padx=8, pady=8,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        tk.Button(
            buttons, text="이미지 저장", command=self.save_image,
            bg="#DB8A73", fg="white", relief="flat", padx=8, pady=8,
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        stage = tk.Frame(self.root, bg="#e6e1d8")
        stage.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(
            stage, width=670, height=650,
            bg="#FFF9FB", highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

    def add_option(self, parent, label, variable, values):
        tk.Label(
            parent, text=label, anchor="w", bg="#fffdf8",
            font=("Noto Sans KR", 10),
        ).pack(fill="x", pady=(7, 2))
        row = tk.Frame(parent, bg="#fffdf8")
        row.pack(fill="x")
        button_map = {}
        for value in values:
            button = tk.Button(
                row,
                text=value,
                relief="flat",
                font=("Noto Sans KR", 9),
                cursor="hand2",
                padx=4,
                pady=3,
                command=lambda selected=value, var=variable: var.set(selected),
            )
            button.pack(side="left", expand=True, fill="x", padx=1)
            button_map[value] = button

        if not hasattr(self, "_option_buttons"):
            self._option_buttons = {}
        self._option_buttons[id(variable)] = (variable, button_map)
        variable.trace_add("write", lambda *_: self.update_option_buttons(variable))
        self.update_option_buttons(variable)

    def update_option_buttons(self, variable):
        _variable, button_map = self._option_buttons[id(variable)]
        for value, button in button_map.items():
            if variable.get() == value:
                button.configure(bg="#E6AFC4", fg="#FFFFFF", activebackground="#D99AAF")
            else:
                button.configure(bg="#F4EEF1", fg="#665F57", activebackground="#E9DEE4")

    def add_color_button(self, parent, label, attribute):
        row = tk.Frame(parent, bg="#fffdf8")
        row.pack(fill="x", pady=3)
        tk.Label(
            row, text=label, width=10, anchor="w", bg="#fffdf8",
            font=("Noto Sans KR", 10),
        ).pack(side="left")
        button = tk.Button(
            row, text="  ", width=4, relief="solid",
            command=lambda: self.choose_color(attribute),
        )
        button.pack(side="right")
        setattr(self, attribute + "_button", button)
        self.update_color_button(attribute)

    def update_color_button(self, attribute):
        getattr(self, attribute + "_button").configure(bg=getattr(self, attribute))

    def choose_color(self, attribute):
        color = colorchooser.askcolor(
            title="색 선택", initialcolor=getattr(self, attribute),
        )[1]
        if color:
            setattr(self, attribute, color)
            self.update_color_button(attribute)
            self.draw_cat()

    def add_slider(self, parent, label, variable, minimum, maximum):
        tk.Label(
            parent, text=label, anchor="w", bg="#fffdf8",
            font=("Noto Sans KR", 10),
        ).pack(fill="x", pady=(7, 0))
        tk.Scale(
            parent, from_=minimum, to=maximum, orient="horizontal",
            variable=variable, command=lambda _value: self.draw_cat(),
            bg="#fffdf8", highlightthickness=0,
        ).pack(fill="x")

    def draw_grid(self):
        self.canvas.create_rectangle(0, 0, 670, 650, fill="#FFF9FB", outline="")

        # Soft pastel decorations keep the background cute but uncluttered.
        decorations = [
            (90, 90, 18, "#F7E1EA"),
            (580, 115, 22, "#E8EEF7"),
            (575, 520, 20, "#F7E6CF"),
            (92, 510, 14, "#E4F1EA"),
        ]
        for cx, cy, radius, color in decorations:
            self.canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill=color, outline="",
            )

        for cx, cy, color in (
            (115, 175, "#EAC6D5"),
            (545, 205, "#CDE1ED"),
            (535, 430, "#ECD6B9"),
            (145, 420, "#D8E8DD"),
        ):
            self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=color, outline="")
            self.canvas.create_oval(cx - 15, cy - 2, cx - 5, cy + 8, fill=color, outline="")
            self.canvas.create_oval(cx + 5, cy - 2, cx + 15, cy + 8, fill=color, outline="")
            self.canvas.create_oval(cx - 12, cy - 12, cx - 4, cy - 4, fill=color, outline="")

    def draw_cat(self, *args):
        self.canvas.delete("all")
        self.draw_grid()

        cx = 335
        fw = self.face_width.get()
        fh = self.face_height.get()
        ear = self.ear_size.get()
        head_left = cx - fw / 2
        head_right = cx + fw / 2
        head_top = 145 - (fh - 270) / 2
        head_bottom = head_top + fh
        outline = "#391F18"

        # Tail is not visible in the seated reference pose.

        # Ears
        ear_height = ear
        left_ear = [
            head_left - 8, head_top + 65,
            head_left + 5, head_top - ear_height - 3,
            cx - 18, head_top + 4,
            cx - 34, head_top + 31,
        ]
        right_ear = [
            cx + 34, head_top + 31,
            cx + 18, head_top + 4,
            head_right - 5, head_top - ear_height - 3,
            head_right + 8, head_top + 65,
        ]
        self.canvas.create_polygon(
            left_ear, fill=self.fur, outline=outline, width=10,
            joinstyle="miter",
        )
        self.canvas.create_polygon(
            right_ear, fill=self.fur, outline=outline, width=10,
            joinstyle="miter",
        )
        self.canvas.create_polygon(
            head_left + 24, head_top + 54,
            head_left + 30, head_top - ear_height + 34,
            cx - 72, head_top + 29,
            cx - 48, head_top + 50,
            fill=self.inner_ear, outline="",
        )
        self.canvas.create_polygon(
            cx + 48, head_top + 50,
            cx + 72, head_top + 29,
            head_right - 30, head_top - ear_height + 34,
            head_right - 24, head_top + 54,
            fill=self.inner_ear, outline="",
        )

        # Seated body behind the head
        body_left = cx - 112
        body_right = cx + 112
        body_top = head_bottom - 50
        body_bottom = 575
        self.canvas.create_oval(
            body_left, body_top, body_right, body_bottom,
            fill=self.fur, outline=outline, width=10,
        )

        # Legs and feet
        for side in (-1, 1):
            foot_x = cx + side * 83
            self.canvas.create_oval(
                foot_x - 30, 540, foot_x + 30, 596,
                fill=self.fur, outline=outline, width=9,
            )

        self.canvas.create_line(
            cx - 55, 500, cx - 55, 580,
            cx - 5, 600, cx - 5, 545,
            fill=outline, width=10, capstyle="round", smooth=True,
        )
        self.canvas.create_line(
            cx + 55, 500, cx + 55, 580,
            cx + 5, 600, cx + 5, 545,
            fill=outline, width=10, capstyle="round", smooth=True,
        )

        # Main head
        self.canvas.create_oval(
            head_left, head_top, head_right, head_bottom,
            fill=self.fur, outline=outline, width=10,
        )

        self.draw_patterns(cx, head_top, fw, fh)
        self.draw_eyes(cx, head_top, fw, fh)
        self.draw_muzzle(cx, head_top, fw, fh)

    def draw_patterns(self, cx, head_top, fw, fh):
        pattern = self.pattern.get()
        if pattern == "단색":
            return

        darker = self.mix_color(self.fur, "#4D4037", 0.30)
        if pattern == "줄무늬":
            for dx in (-38, 0, 38):
                self.canvas.create_line(
                    cx + dx, head_top + 45,
                    cx + dx * 0.55, head_top + 95,
                    fill=darker, width=7, smooth=True,
                )
        elif pattern == "점무늬":
            for dx, dy in (
                (-75, 70), (-45, 112), (45, 112),
                (75, 70), (-100, 145), (100, 145),
            ):
                self.canvas.create_oval(
                    cx + dx - 7, head_top + dy - 7,
                    cx + dx + 7, head_top + dy + 7,
                    fill=darker, outline="",
                )
        elif pattern == "삼색":
            dark = "#514A46"
            cream = "#F0E0BD"
            self.canvas.create_oval(
                cx - fw * 0.34, head_top + 20,
                cx - fw * 0.08, head_top + 115,
                fill=dark, outline="",
            )
            self.canvas.create_oval(
                cx + fw * 0.08, head_top + 15,
                cx + fw * 0.31, head_top + 105,
                fill=cream, outline="",
            )

    def draw_eyes(self, cx, head_top, fw, fh):
        eye_r = self.eye_size.get()
        eye_y = head_top + 145
        expression = self.expression.get()

        for eye_x in (cx - fw * 0.24, cx + fw * 0.24):
            if expression == "졸림":
                self.canvas.create_arc(
                    eye_x - eye_r - 4, eye_y - eye_r,
                    eye_x + eye_r + 4, eye_y + eye_r,
                    start=0, extent=180, style="arc",
                    width=6, outline="#391F18",
                )
                continue

            if expression == "신비":
                self.canvas.create_arc(
                    eye_x - eye_r, eye_y - eye_r,
                    eye_x + eye_r, eye_y + eye_r,
                    start=15, extent=150, style="arc",
                    width=5, outline="#391F18",
                )
                continue

            self.canvas.create_oval(
                eye_x - eye_r, eye_y - eye_r,
                eye_x + eye_r, eye_y + eye_r,
                fill=self.eye, outline="#391F18", width=2,
            )

            shape = self.pupil_shape.get()
            if shape == "세로":
                pw, ph = 5, eye_r * 0.58
                self.canvas.create_oval(
                    eye_x - pw, eye_y - ph,
                    eye_x + pw, eye_y + ph,
                    fill=self.pupil, outline="",
                )
            elif shape == "둥근":
                pr = eye_r * 0.38
                self.canvas.create_oval(
                    eye_x - pr, eye_y - pr,
                    eye_x + pr, eye_y + pr,
                    fill=self.pupil, outline="",
                )
            else:
                pr = 4
                self.canvas.create_oval(
                    eye_x - pr, eye_y - pr,
                    eye_x + pr, eye_y + pr,
                    fill=self.pupil, outline="",
                )

            self.canvas.create_oval(
                eye_x - eye_r * 0.48, eye_y - eye_r * 0.50,
                eye_x - eye_r * 0.12, eye_y - eye_r * 0.14,
                fill="#FFFFFF", outline="",
            )

        # Eyebrows
        self.canvas.create_arc(
            cx - fw * 0.33, head_top + 54,
            cx - fw * 0.20, head_top + 82,
            start=20, extent=150, style="arc",
            width=8, outline="#A36F52",
        )
        self.canvas.create_arc(
            cx + fw * 0.20, head_top + 54,
            cx + fw * 0.33, head_top + 82,
            start=190, extent=150, style="arc",
            width=8, outline="#A36F52",
        )

    def draw_muzzle(self, cx, head_top, fw, fh):
        muzzle_y = head_top + 205

        # Blush
        blush = "#F4A5A5"
        for eye_x in (cx - fw * 0.33, cx + fw * 0.33):
            self.canvas.create_oval(
                eye_x - 32, muzzle_y - 38,
                eye_x + 32, muzzle_y - 10,
                fill=blush, outline="",
            )

        # Nose
        self.canvas.create_polygon(
            cx - 12, muzzle_y - 54,
            cx + 12, muzzle_y - 54,
            cx, muzzle_y - 39,
            fill=self.nose, outline="#391F18", width=3,
            smooth=True,
        )

        expression = self.expression.get()
        if expression == "행복":
            self.canvas.create_arc(
                cx - 28, muzzle_y - 50,
                cx, muzzle_y - 18,
                start=180, extent=160, style="arc",
                width=4, outline="#391F18",
            )
            self.canvas.create_arc(
                cx, muzzle_y - 50,
                cx + 28, muzzle_y - 18,
                start=180, extent=160, style="arc",
                width=4, outline="#391F18",
            )
        elif expression == "신비":
            self.canvas.create_line(
                cx - 14, muzzle_y - 25,
                cx - 2, muzzle_y - 18,
                cx + 16, muzzle_y - 31,
                width=4, fill="#391F18", smooth=True,
            )
            self.canvas.create_line(
                cx - 4, muzzle_y - 25,
                cx - 4, muzzle_y - 10,
                width=3, fill="#391F18",
            )
        elif expression == "차분":
            self.canvas.create_line(
                cx - 18, muzzle_y - 24,
                cx + 18, muzzle_y - 24,
                width=4, fill="#391F18", smooth=True,
            )
        else:
            self.canvas.create_arc(
                cx - 18, muzzle_y - 38,
                cx + 18, muzzle_y - 12,
                start=0, extent=180, style="arc",
                width=4, outline="#391F18",
            )

    def randomize(self):
        fur_colors = ["#FFFDF8", "#F3C47F", "#A9A29A", "#D8A47F",
                      "#D9BFA5", "#7C6C63", "#E8DFC6", "#B55F55"]
        eye_colors = ["#79A85B", "#59A0C5", "#D3A43A", "#87A96B",
                      "#8C79A8", "#70C1A2", "#3A211C"]
        nose_colors = ["#C86A75", "#A67872", "#D39AA5", "#3A211C"]

        self.fur = random.choice(fur_colors)
        self.eye = random.choice(eye_colors)
        self.pupil = random.choice(["#171717", "#263238", "#101010"])
        self.nose = random.choice(nose_colors)
        self.inner_ear = random.choice(["#F5A4A1", "#E6A2A8", "#C98D86", "#F1BDC1"])
        self.pupil_shape.set(random.choice(["세로", "둥근", "작은 점"]))
        self.expression.set(random.choice(["행복", "차분", "신비", "졸림"]))
        self.pattern.set(random.choice(["단색", "줄무늬", "점무늬", "삼색"]))

        for attribute in ("fur", "eye", "pupil", "nose"):
            self.update_color_button(attribute)
        self.draw_cat()

    def save_image(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("EPS 이미지", "*.eps"), ("PostScript", "*.ps")],
            title="고양이 이미지 저장",
        )
        if not path:
            return

        try:
            self.canvas.postscript(file=path, colormode="color")
            messagebox.showinfo("저장 완료", f"고양이 이미지를 저장했습니다.\n{path}")
        except Exception as exc:
            messagebox.showerror("저장 실패", str(exc))

    @staticmethod
    def mix_color(base, target, amount):
        base = base.lstrip("#")
        target = target.lstrip("#")
        br, bg, bb = (int(base[i:i + 2], 16) for i in (0, 2, 4))
        tr, tg, tb = (int(target[i:i + 2], 16) for i in (0, 2, 4))
        return "#{:02X}{:02X}{:02X}".format(
            int(br + (tr - br) * amount),
            int(bg + (tg - bg) * amount),
            int(bb + (tb - bb) * amount),
        )


def main():
    root = tk.Tk()
    CatDesigner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
