import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.cm as cm
import numpy as np

canvas = None
df = None
current_file = None

def load_file():
    global canvas, df, current_file

    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path, sep=";")
        df["X"] = df["X"].astype(str).str.replace(",", ".").astype(float)
        df["Y"] = df["Y"].astype(str).str.replace(",", ".").astype(float)
        current_file = file_path
    except Exception as e:
        messagebox.showerror("Hata", f"Dosya okunurken bir hata oluştu: {e}")
        return

    draw_pcb()


def refresh_canvas():
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    draw_pcb()


def draw_pcb():
    global canvas, df

    boyut = 10
    max_x, max_y = df["X"].max() + boyut, df["Y"].max() + boyut

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor("forestgreen")
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_title("PCB Komponent Yerleşimi")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")

    packages = df["Package"].unique()
    colors = cm.tab20(np.linspace(0, 1, len(packages)))
    color_map = dict(zip(packages, colors))

    def rotate_point(x, y, cx, cy, angle):
        rad = np.deg2rad(angle)
        cos = np.cos(rad)
        sin = np.sin(rad)
        qx = cx + cos * (x - cx) - sin * (y - cy)
        qy = cy + sin * (x - cx) + cos * (y - cy)
        return qx, qy

    for _, row in df.iterrows():
        ref = row["Ref"]
        x, y, r = row["X"], row["Y"], row["R"]
        package = str(row["Package"]).strip()

        if package.startswith("R"):
            body_w, body_h = 2.0, 1.2
            pad_w, pad_h = 1.0, 1.2
            rect = plt.Rectangle((x - body_w / 2, y - body_h / 2), body_w, body_h,
                                 facecolor=color_map[package], edgecolor='black')
            ax.add_patch(rect)
            pad1 = plt.Rectangle((x - body_w / 2 - pad_w, y - pad_h / 2), pad_w, pad_h,
                                 facecolor='gray', edgecolor='black')
            ax.add_patch(pad1)
            pad2 = plt.Rectangle((x + body_w / 2, y - pad_h / 2), pad_w, pad_h,
                                 facecolor='gray', edgecolor='black')
            ax.add_patch(pad2)
            rect.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)
            pad1.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)
            pad2.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

        elif package == "MELF":
            body_w, body_h = 5.2, 2.5
            rect = plt.Rectangle((x - body_w / 2, y - body_h / 2), body_w, body_h,
                                 facecolor=color_map[package], edgecolor='black')
            ax.add_patch(rect)
            rect.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

        elif "SOIC" in package:
            body_w, body_h = 6.0, 4.0
            pin_w, pin_h = 0.5, 2.0
            pin_count = int(package.split('-')[0]) if '-' in package else 8
            pin_spacing = (body_h - (pin_count / 2 - 1) * 1.27) / 2
            rect = plt.Rectangle((x - body_w / 2, y - body_h / 2), body_w, body_h,
                                 facecolor=color_map[package], edgecolor='black')
            ax.add_patch(rect)
            rect.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)
            for i in range(pin_count // 2):
                pin_x_left = x - body_w / 2 - pin_h
                pin_y_left = y - body_h / 2 + pin_spacing + i * 1.27
                left_pin = plt.Rectangle((pin_x_left, pin_y_left), pin_h, pin_w,
                                         facecolor='gray', edgecolor='black')
                ax.add_patch(left_pin)
                left_pin.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

                pin_x_right = x + body_w / 2
                pin_y_right = y - body_h / 2 + pin_spacing + i * 1.27
                right_pin = plt.Rectangle((pin_x_right, pin_y_right), pin_h, pin_w,
                                          facecolor='gray', edgecolor='black')
                ax.add_patch(right_pin)
                right_pin.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

        elif "PQFN" in package or "QFN" in package:
            body_w, body_h = 4.0, 4.0
            pin_w, pin_h = 0.5, 1.0
            pin_count = int(package.split('-')[0]) if '-' in package else 8

            rect = plt.Rectangle((x - body_w / 2, y - body_h / 2), body_w, body_h,
                                 facecolor=color_map[package], edgecolor='black')
            ax.add_patch(rect)
            rect.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

            if pin_count == 8:
                for i in range(4):
                    pad_x = x - 1.5 + i * 1.0
                    top_pad = plt.Rectangle((pad_x, y + body_h/2), pin_w, pin_h,
                                            facecolor='gray', edgecolor='black')
                    ax.add_patch(top_pad)
                    top_pad.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

                    bottom_pad = plt.Rectangle((pad_x, y - body_h/2 - pin_h), pin_w, pin_h,
                                               facecolor='gray', edgecolor='black')
                    ax.add_patch(bottom_pad)
                    bottom_pad.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

        elif "4-SMD" in package:
            body_w, body_h = 4.0, 3.0
            pin_w, pin_h = 1.0, 0.5
            rect = plt.Rectangle((x - body_w/2, y - body_h/2), body_w, body_h,
                                 facecolor=color_map[package], edgecolor='black')
            ax.add_patch(rect)
            rect.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

            for i in range(2):
                pad_y = y - body_h/2 + (i+0.5)*body_h/2
                pad = plt.Rectangle((x - body_w/2 - pin_w, pad_y), pin_w, pin_h,
                                    facecolor='gray', edgecolor='black')
                ax.add_patch(pad)
                pad.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

            for i in range(2):
                pad_y = y - body_h/2 + (i+0.5)*body_h/2
                pad = plt.Rectangle((x + body_w/2, pad_y), pin_w, pin_h,
                                    facecolor='gray', edgecolor='black')
                ax.add_patch(pad)
                pad.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

            circle = plt.Circle((x - body_w/2 + 0.5, y + body_h/2 - 0.5),
                                0.3, facecolor='white', edgecolor='black')
            ax.add_patch(circle)
            circle.set_transform(plt.matplotlib.transforms.Affine2D().rotate_deg_around(x, y, r) + ax.transData)

        elif package == "LABEL":
            text_x, text_y = rotate_point(x, y, x, y, r)
            ax.text(text_x, text_y, ref, ha="center", va="center", fontsize=8, color='black', picker=True)
            continue
        else:
            ax.plot(x, y, 'o', color=color_map[package], markersize=10)

        if package != "LABEL":
            text_x, text_y = rotate_point(x, y, x, y, r)
            ax.text(text_x, text_y, ref, ha="center", va="center", fontsize=8,
                    color='black', picker=True, rotation=r)

    def on_pick(event):
        artist = event.artist
        if isinstance(artist, plt.Text):
            text = artist.get_text()
            comp_index = df[df["Ref"] == text].index[0]
            comp_data = df.loc[comp_index]

            win = tk.Toplevel(root)
            win.title("Komponent Bilgisi")

            info_label = tk.Label(win, justify="left")
            info_label.pack(pady=10)

            def update_info():
                comp = df.loc[comp_index]
                new_info = (f"Ref: {comp['Ref']}\n"
                            f"Comp: {comp['Comp']}\n"
                            f"X: {comp['X']}\n"
                            f"Y: {comp['Y']}\n"
                            f"R: {comp['R']}\n"
                            f"Package: {comp['Package']}")
                info_label.config(text=new_info)

            def rotate_component():
                df.at[comp_index, "R"] = (df.at[comp_index, "R"] + 90) % 360
                df.to_csv(current_file, sep=";", index=False)
                refresh_canvas()
                update_info()

            btn = tk.Button(win, text="Döndür (+90°)", command=rotate_component)
            btn.pack(pady=5)

            update_info()

    fig.canvas.mpl_connect("pick_event", on_pick)

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("PCB Viewer")
btn = tk.Button(root, text="Dosya Seç ve Yükle", command=load_file)
btn.pack(pady=10)
root.mainloop()
