import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Функція Гаусса з умовою Б
def gauss(t, A, mu, b1, b2):
    b = np.where(t < mu, b1, b2)
    return A * np.exp(-((t - mu) ** 2) / (2 * b ** 2))

# Функція генерації графіка ЕКГ(один цикл)
def generate_ecg(*args):
    global last_valid_values
    HC = hc_slider.get()
    AT = at_slider.get()
    mu_T_relative = mu_t_slider.get()
    b1_T = b1_t_slider.get()
    b2_T = b2_t_slider.get()

    T0 = (60 * 1000) / HC
    t = np.arange(0, T0, 2)

    mu_P = 0.25 * T0
    mu_Q = 0.35 * T0
    mu_R = 0.45 * T0
    mu_S = 0.52 * T0
    mu_ST = 0.57 * T0
    mu_T = mu_T_relative * T0

    b1_P, b2_P = 15, 15
    b1_Q, b2_Q = 5, 5
    b1_R, b2_R = 6, 6
    b1_S, b2_S = 5, 5
    b1_ST, b2_ST = 10, 10

    t_P1, t_P2 = mu_P - 3 * b1_P, mu_P + 3 * b2_P
    t_Q1, t_Q2 = mu_Q - 3 * b1_Q, mu_Q + 3 * b2_Q
    t_R1, t_R2 = mu_R - 3 * b1_R, mu_R + 3 * b2_R
    t_S1, t_S2 = mu_S - 3 * b1_S, mu_S + 3 * b2_S
    t_ST1, t_ST2 = mu_ST - 3 * b1_ST, mu_ST + 3 * b2_ST
    t_T1, t_T2 = mu_T - 3 * b1_T, mu_T + 3 * b2_T

    constraint_satisfied = (0 <= t_P1 < t_P2 <= t_Q1 < t_Q2 <= t_R1 < t_R2 <= t_S1 < t_S2 <= t_ST1 < t_ST2 <= t_T1 < t_T2 <= T0)

    if not constraint_satisfied:
        mu_t_slider.set(last_valid_values['mu_t'])
        b1_t_slider.set(last_valid_values['b1_t'])
        b2_t_slider.set(last_valid_values['b2_t'])
        return

    last_valid_values = {'mu_t': mu_T_relative, 'b1_t': b1_T, 'b2_t': b2_T}

    ecg = (gauss(t, 0.25, mu_P, b1_P, b2_P) +
           gauss(t, -0.15, mu_Q, b1_Q, b2_Q) +
           gauss(t, 1.0, mu_R, b1_R, b2_R) +
           gauss(t, -0.2, mu_S, b1_S, b2_S) +
           gauss(t, 0.0, mu_ST, b1_ST, b2_ST) +
           gauss(t, AT, mu_T, b1_T, b2_T))

    ax.clear()
    ax.plot(t / 1000, ecg, label='ЕКГ', linewidth=1)  #переводимо час в секунди
    ax.set_title("ЕКГ модель")
    ax.set_xlabel('Час (с)')
    ax.set_ylabel('Амплітуда (мВ)')
    ax.legend()
    ax.grid()

    boundaries = [
        ('P', t_P1, t_P2, 'green'),
        ('Q', t_Q1, t_Q2, 'red'),
        ('R', t_R1, t_R2, 'blue'),
        ('S', t_S1, t_S2, 'purple'),
        ('ST', t_ST1, t_ST2, 'orange'),
        ('T', t_T1, t_T2, 'brown')
    ]

    for name, start, end, color in boundaries:
        ax.axvline(x=start / 1000, color=color, linestyle='--', alpha=0.5)
        ax.axvline(x=end / 1000, color=color, linestyle='--', alpha=0.5)
        ax.text((start + end) / 2 / 1000, 0, name, color=color, ha='center')

    canvas.draw()

# Функція для генерації одного циклу ЕКГ
def generate_single_cycle(t, T0, cycle_index, AT, mu_T_relative, b1_T, b2_T, delta_A):
    mu_P = 0.25 * T0
    mu_Q = 0.35 * T0
    mu_R = 0.45 * T0
    mu_S = 0.52 * T0
    mu_ST = 0.57 * T0
    mu_T = mu_T_relative * T0

    b1_P, b2_P = 15, 15
    b1_Q, b2_Q = 5, 5
    b1_R, b2_R = 6, 6
    b1_S, b2_S = 5, 5
    b1_ST, b2_ST = 10, 10

    # Альтернация зубца T
    lambda_T = lambda_values[cycle_index]
    A_T = AT * lambda_T

    ecg = (gauss(t, 0.25, mu_P, b1_P, b2_P) +
           gauss(t, -0.15, mu_Q, b1_Q, b2_Q) +
           gauss(t, 1.0, mu_R, b1_R, b2_R) +
           gauss(t, -0.2, mu_S, b1_S, b2_S) +
           gauss(t, 0.0, mu_ST, b1_ST, b2_ST) +
           gauss(t, A_T, mu_T, b1_T, b2_T))

    return ecg

# Функція для відкриття вікна генерації
def open_generation_window():
    generation_window = tk.Toplevel(root)
    generation_window.title("Генерація ЕКГ з альтернацією зубця T")

    # Фрейм для елементів керування
    controls_frame = ttk.Frame(generation_window)
    controls_frame.pack(pady=5)

    num_cycles_label = ttk.Label(controls_frame, text="Кількість циклів:")
    num_cycles_label.pack(side=tk.LEFT, padx=5)
    num_cycles_var = tk.StringVar(value="30")
    num_cycles_entry = ttk.Entry(controls_frame, textvariable=num_cycles_var, width=5)
    num_cycles_entry.pack(side=tk.LEFT, padx=5)

    at_alternation_label = ttk.Label(controls_frame, text="Рівень альтернації зубця T:")
    at_alternation_label.pack(side=tk.LEFT, padx=5)
    at_alternation_var = tk.DoubleVar(value=0.5)
    at_alternation_slider = tk.Scale(controls_frame, from_=0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=at_alternation_var)
    at_alternation_slider.pack(side=tk.LEFT, padx=5)

    noise_level_label = ttk.Label(controls_frame, text="Рівень шуму:")
    noise_level_label.pack(side=tk.LEFT, padx=5)
    noise_level_var = tk.DoubleVar(value=0)
    noise_level_slider = tk.Scale(controls_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=noise_level_var)
    noise_level_slider.pack(side=tk.LEFT, padx=5)

    fig_gen, ax_gen = plt.subplots(figsize=(10, 5))
    canvas_gen = FigureCanvasTkAgg(fig_gen, master=generation_window)
    # Зміна ширини та висоти для canvas
    canvas_gen.get_tk_widget().config(width=1800,
                                      height=400)  #Можна змінити ці значення, щоб отримати більшу ширину

    canvas_gen.get_tk_widget().pack(pady=10)

    def generate_ecg_with_alternation(*args):
        num_cycles = int(num_cycles_var.get())
        delta_A = at_alternation_var.get()
        noise_level = noise_level_var.get()

        HC = hc_slider.get()
        AT = at_slider.get()
        mu_T_relative = mu_t_slider.get()
        b1_T = b1_t_slider.get()
        b2_T = b2_t_slider.get()

        T0 = (60 * 1000) / HC
        t = np.arange(0, T0 * num_cycles, 2)
        ecg_signal = np.zeros_like(t)

        # Генерація значень lambda для альтернації зубця T
        global lambda_values
        lambda_values = [1]  # Початкове значення lambda_0^(T) = 1
        for m in range(1, num_cycles):
            if lambda_values[m - 1] == 1:
                lambda_values.append(1 + delta_A / AT)
            else:
                lambda_values.append(1)

        # Генерація циклів ЕКГ
        for i in range(num_cycles):
            t_shifted = t - i * T0
            mask = (t_shifted >= 0) & (t_shifted < T0)
            ecg_cycle = generate_single_cycle(t_shifted[mask], T0, i, AT, mu_T_relative, b1_T, b2_T, delta_A)
            ecg_signal[mask] += ecg_cycle

        # Додавання шуму
        noise = np.random.normal(0, noise_level, len(ecg_signal))
        ecg_signal += noise

        ax_gen.clear()
        ax_gen.plot(t / 1000, ecg_signal, linewidth=1)

        # Зменшуємо масштаб осі X (час) и осі Y (амплітупд)
        ax_gen.set_xlim([0, t[-1] / 1000])
        ax_gen.set_ylim([np.min(ecg_signal) * 1.1, np.max(ecg_signal) * 1.1])  # 

        ax_gen.set_title("ЕКГ з альтернацією зубця T")
        ax_gen.set_xlabel('Час (с)')
        ax_gen.set_ylabel('Амплітуда (мВ)')
        ax_gen.grid()
        canvas_gen.draw()

    # Прив'язка оновлення графіка до змін параметрів
    num_cycles_var.trace("w", generate_ecg_with_alternation)
    at_alternation_var.trace("w", generate_ecg_with_alternation)
    noise_level_var.trace("w", generate_ecg_with_alternation)
    hc_slider.bind("<ButtonRelease-1>", generate_ecg_with_alternation)
    at_slider.bind("<ButtonRelease-1>", generate_ecg_with_alternation)
    mu_t_slider.bind("<ButtonRelease-1>", generate_ecg_with_alternation)
    b1_t_slider.bind("<ButtonRelease-1>", generate_ecg_with_alternation)
    b2_t_slider.bind("<ButtonRelease-1>", generate_ecg_with_alternation)

    # Початкова генерація
    generate_ecg_with_alternation()

# Основне вікно
root = tk.Tk()
root.title("My ECG")

main_frame = ttk.Frame(root)
main_frame.grid(column=0, row=0, sticky="nsew")

fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

controls_frame = ttk.Frame(main_frame)
controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

last_valid_values = {'mu_t': 0.7, 'b1_t': 10, 'b2_t': 15}

hc_slider = tk.Scale(controls_frame, from_=40, to=65, label="Частота СС (уд/хв)", orient=tk.HORIZONTAL, command=generate_ecg)
hc_slider.set(60)
hc_slider.pack(fill="x", pady=5)

at_slider = tk.Scale(controls_frame, from_=0.1, to=1.5, resolution=0.1, label="Амплітуда T", orient=tk.HORIZONTAL, command=generate_ecg)
at_slider.set(0.5)
at_slider.pack(fill="x", pady=5)

mu_t_slider = tk.Scale(controls_frame, from_=0.5, to=0.9, resolution=0.01, label="Момент екстр. T", orient=tk.HORIZONTAL, command=generate_ecg)
mu_t_slider.set(0.7)
mu_t_slider.pack(fill="x", pady=5)

b1_t_slider = tk.Scale(controls_frame, from_=5, to=20, label="b1 T", orient=tk.HORIZONTAL, command=generate_ecg)
b1_t_slider.set(10)
b1_t_slider.pack(fill="x", pady=5)

b2_t_slider = tk.Scale(controls_frame, from_=5, to=20, label="b2 T", orient=tk.HORIZONTAL, command=generate_ecg)
b2_t_slider.set(15)
b2_t_slider.pack(fill="x", pady=5)

generate_button = ttk.Button(controls_frame, text="ГЕНЕРАЦІЯ", command=open_generation_window)
generate_button.pack(pady=10)

generate_ecg()

root.mainloop()
