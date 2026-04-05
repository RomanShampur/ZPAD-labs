import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import savgol_filter

#функція для генерації гармоніки
def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    harmonic = amplitude * np.sin(frequency * t + phase)
    #створюємо шум окремо
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
    result = harmonic + noise if show_noise else harmonic
    return result, harmonic, noise

plt.close('all')

#параметри часу
t = np.linspace(0, 10, 1000)
init_amp, init_freq, init_phase = 1.0, 2.0, 0.0
init_n_mean, init_n_cov = 0.0, 0.1

#створення фігури
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.35, hspace=0.4)

#початкові дані
y_full, h_pure, n_current = harmonic_with_noise(t, init_amp, init_freq, init_phase, init_n_mean, init_n_cov, True)
y_filt_init = savgol_filter(y_full, 51, 3)

#графіки
line_noisy, = ax1.plot(t, y_full, color='orange', lw=1, label='Зашумлена', alpha=0.6)
line_ref_top, = ax1.plot(t, h_pure, color='blue', linestyle='--', lw=1.5, label='Еталон')
line_filt_top, = ax1.plot(t, y_filt_init, color='purple', lw=2, label='Фільтрація (Savgol)')

ax1.set_title("Вхідний сигнал: шум + еталон + фільтр")
ax1.set_ylim(-5, 5)
ax1.legend(loc='upper right', fontsize='x-small', ncol=3)
ax1.grid(True, linestyle=':', alpha=0.5)

line_pure_filt, = ax2.plot(t, y_filt_init, color='green', lw=2.5, label='Результат очищення')
ax2.set_title("Результат: чиста відфільтрована функція")
ax2.set_ylim(-5, 5)
ax2.legend(loc='upper right')
ax2.grid(True, linestyle=':', alpha=0.5)

#віджети
ax_color = 'ghostwhite'
s_amp = Slider(plt.axes([0.15, 0.22, 0.3, 0.03], facecolor=ax_color), 'Ампл.', 0.1, 4.0, valinit=init_amp)
s_freq = Slider(plt.axes([0.15, 0.18, 0.3, 0.03], facecolor=ax_color), 'Част.', 0.1, 10.0, valinit=init_freq)
s_phase = Slider(plt.axes([0.15, 0.14, 0.3, 0.03], facecolor=ax_color), 'Фаза', 0, 2*np.pi, valinit=init_phase)

s_n_mean = Slider(plt.axes([0.6, 0.22, 0.25, 0.03], facecolor=ax_color), 'Сер.шум', -2.0, 2.0, valinit=init_n_mean)
s_n_cov = Slider(plt.axes([0.6, 0.18, 0.25, 0.03], facecolor=ax_color), 'Дисп.', 0.0, 2.0, valinit=init_n_cov)

ax_check = plt.axes([0.6, 0.05, 0.15, 0.08])
check = CheckButtons(ax_check, ('Шум', 'Фільтр'), (True, True))
btn_reset = Button(plt.axes([0.8, 0.05, 0.12, 0.05]), 'Скинути', color='lightcoral')

def update(val):
    show_noise_status, show_filter_status = check.get_status()
    
    #створюємо нову гармоніку на основі слайдерів
    y_res, h_new, n_new = harmonic_with_noise(t, s_amp.val, s_freq.val, s_phase.val, s_n_mean.val, s_n_cov.val, True)
    
    #фільтруємо сигнал (завжди зашумлений для обробки)
    y_filt_updated = savgol_filter(y_res, 51, 3)
    
    #оновлюємо лінії
    line_ref_top.set_ydata(h_new)
    line_noisy.set_ydata(y_res)
    line_noisy.set_visible(show_noise_status)
    
    line_filt_top.set_ydata(y_filt_updated)
    line_filt_top.set_visible(show_filter_status)
    
    line_pure_filt.set_ydata(y_filt_updated)
    
    fig.canvas.draw_idle()

#зв'язування подій
s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_n_mean.on_changed(update)
s_n_cov.on_changed(update)
check.on_clicked(lambda label: update(None))
btn_reset.on_clicked(lambda event: [s.reset() for s in [s_amp, s_freq, s_phase, s_n_mean, s_n_cov]])

plt.show()