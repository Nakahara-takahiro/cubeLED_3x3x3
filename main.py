import machine
import time

# 設定
PCYCLE = 360  # ms
# カラム（PNP+NPN: HighでON/点灯）
COL_PINS = [3, 4, 1, 7, 8, 6, 10, 11, 9]
# レイヤー（NPN等: HighでON/点灯）
LAY_PINS = [13, 14, 15]

# オンボードLED(ヘルスチェック)
try:
    led_onboard = machine.Pin("LED", machine.Pin.OUT)
except:
    led_onboard = machine.Pin(25, machine.Pin.OUT)

# --- パターンデータ (0b 3列_2列_1列) ---
PTN = [
    [0b000_000_000, 0b000_000_000, 0b111_111_111], # 下層
    [0b000_000_000, 0b111_111_111, 0b111_111_111], # 下・中層
    [0b111_111_111, 0b111_111_111, 0b111_111_111], # 全層
    [0b000_100_000, 0b000_100_000, 0b000_100_000], # 柱
    [0b101_010_101, 0b010_101_010, 0b101_010_101], # 市松模様
]

# ピンの初期化
# 正論理になったので、初期値はすべて 0 (OFF) にします
col_pins = [machine.Pin(p, machine.Pin.OUT, value=0) for p in COL_PINS]
lay_pins = [machine.Pin(p, machine.Pin.OUT, value=0) for p in LAY_PINS]

def run_cube():
    last_heartbeat = time.ticks_ms()
    print("LED Cube Start! (Active-High Mode)")
    
    while True:
        for pattern in PTN:
            start_time = time.ticks_ms()
            
            while time.ticks_diff(time.ticks_ms(), start_time) < PCYCLE:
                # ヘルスチェック
                if time.ticks_diff(time.ticks_ms(), last_heartbeat) > 500:
                    led_onboard.toggle()
                    last_heartbeat = time.ticks_ms()
                
                # ダイナミック点灯：レイヤーごとにスキャン
                for i in range(3):
                    layer_data = pattern[i]
                    
                    # 1. 前の階の残像を消すために一旦すべてOFF
                    for lp in lay_pins: lp.value(0)
                    for cp in col_pins: cp.value(0)
                    time.sleep_us(200) # 短いデッドタイム

                    # 2. カラムのセット（ここが正論理！）
                    for j in range(9):
                        # layer_dataが1のとき、Picoからも1(High)を出す
                        bit = (layer_data >> j) & 1
                        col_pins[j].value(bit) 
                    
                    # 3. レイヤーON
                    lay_pins[i].value(1)
                    time.sleep_ms(4) # あなたが調整した「チラつかない時間」
                    
                    # 4. レイヤーOFF
                    lay_pins[i].value(0)

if __name__ == "__main__":
    try:
        run_cube()
    except KeyboardInterrupt:
        # 安全停止（すべて0にする）
        for p in col_pins: p.value(0)
        for p in lay_pins: p.value(0)
        led_onboard.value(0)
        print("Stopped.")