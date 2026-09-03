import time
import random
import pyautogui
import pygetwindow as gw

pyautogui.PAUSE = 0.2

# --- HÀM CLICK CHẮC CHẮN (CHỐNG TRƯỢT/MẤT FOCUS) ---

def clean_chrome_tabs():
    """Chỉ đóng đúng cửa sổ Google Chrome, an toàn tuyệt đối."""
    print("\n--- TIẾN HÀNH ĐÓNG CỬA SỔ CHROME ---")

    try:
        chrome_windows = gw.getWindowsWithTitle("Chrome")
        if chrome_windows:
            # Lấy đúng cửa sổ Chrome và ra lệnh đóng
            chrome_win = chrome_windows[0]
            chrome_win.close()
            time.sleep(0.3)
            # Vượt qua popup nếu web có hộp thoại hỏi xác nhận rời trang
            pyautogui.press('enter')
            print("-> Đã đóng cửa sổ Chrome thành công.\n")
        else:
            print("-> Không tìm thấy cửa sổ Chrome nào đang mở.\n")
    except Exception as e:
        print(f"-> Gặp lỗi khi đóng cửa sổ Chrome: {e}\n")

    # Trả lại focus cho cửa sổ Telegram Game
    solid_click(1100, 300)
    time.sleep(0.3)

def solid_click(x, y):
    """Click dứt khoát và giữ chuột nhẹ để nhận tương tác webapp."""
    offset_x = random.randint(-2, 2)
    offset_y = random.randint(-2, 2)
    target_x = x + offset_x
    target_y = y + offset_y

    pyautogui.moveTo(target_x, target_y, duration=0.25)
    time.sleep(0.08)
    pyautogui.mouseDown()
    time.sleep(0.12)
    pyautogui.mouseUp()
    time.sleep(0.1)

def wait_and_click(image_name, check_interval=0.6, confidence=0.65, grayscale=True):
    """Tìm ảnh liên tục trên màn hình (vô hạn thời gian) cho đến khi thấy mới click và đi tiếp."""
    print(f"-> Đang quét tìm: {image_name}...")
    while True:
        try:
            pos = pyautogui.locateCenterOnScreen(image_name, confidence=confidence, grayscale=grayscale)
            if pos:
                print(f"[OK] Đã tìm thấy và bấm: {image_name}")
                solid_click(pos.x, pos.y)
                return True
        except Exception:
            pass
        time.sleep(check_interval + random.uniform(0.05, 0.15))

def check_and_click_if_exists(image_name, check_interval=0.6, confidence=0.65, grayscale=True):
    """Quét liên tục trên màn hình đến khi nào thấy nút mới click và hoàn thành."""
    print(f"-> Đang tìm popup/nút: {image_name}...")
    while True:
        try:
            pos = pyautogui.locateCenterOnScreen(image_name, confidence=confidence, grayscale=grayscale)
            if pos:
                print(f"[OK] Đã tìm thấy và bấm: {image_name}")
                solid_click(pos.x, pos.y)
                time.sleep(0.5)
                return True
        except Exception:
            pass
        time.sleep(check_interval + random.uniform(0.05, 0.15))


# --- QUY TRÌNH FARM TAB ANIMAL ---

def wait_for_watch_ad_or_collect():
    """Chờ nút Watch Ad vô hạn thời gian, tự động nhận thưởng nếu có popup Level Up hoặc nút Collect."""
    print(f"1. Đang chờ nút 'Watch Ad' (Quét kèm Collect All & Claim Rewards nếu có)...")
    while True:
        # Case 1: Thu hoạch trứng/nông sản
        try:
            pos_collect = pyautogui.locateCenterOnScreen("btn_collect_all.png", confidence=0.7, grayscale=False)
            if pos_collect:
                print("[OK] Phát hiện nút 'Collect All' -> Thu hoạch ngay!")
                solid_click(pos_collect.x, pos_collect.y)
                time.sleep(0.5)
        except Exception:
            pass

        # Case 2: Nhận thưởng lên cấp (Level Up Claim Rewards)
        try:
            pos_claim = pyautogui.locateCenterOnScreen("btn_claim_rewards.png", confidence=0.65, grayscale=True)
            if pos_claim:
                print("[OK] Phát hiện popup Level Up -> Bấm 'CLAIM REWARDS'!")
                solid_click(pos_claim.x, pos_claim.y)
                time.sleep(0.5)
        except Exception:
            pass

        # Case 3: Nút xem quảng cáo chính để tiếp tục luồng
        try:
            pos_watch = pyautogui.locateCenterOnScreen("btn_watch_ad.png", confidence=0.7, grayscale=False)
            if pos_watch:
                print("[OK] Đã thấy và bấm: btn_watch_ad.png")
                solid_click(pos_watch.x, pos_watch.y)
                return True
        except Exception:
            pass

        time.sleep(0.5 + random.uniform(0.1, 0.2))

def handle_step_verify():
    """Xử lý bước Verify Visit: Quét liên tục đến khi Verify sáng hoặc Open Link xuất hiện."""
    print("4. Chờ nút 'VERIFY VISIT' sáng (hoặc Open Link)...")
    start_time = time.time()

    while True:
        # Kiểm tra nút Verify sáng
        try:
            pos_v = pyautogui.locateCenterOnScreen("btn_verify_enabled.png", confidence=0.65, grayscale=False)
            if pos_v:
                print("[OK] Nút VERIFY VISIT đã sáng!")
                solid_click(pos_v.x, pos_v.y)
                return True
        except Exception:
            pass

        # Nếu sau 2s chưa sáng thì tìm nút Open Link
        if time.time() - start_time > 2:
            try:
                pos_open = pyautogui.locateCenterOnScreen("btn_open_link.png", confidence=0.65, grayscale=True)
                if pos_open:
                    print("[OK] Đã tìm thấy và bấm: btn_open_link.png")
                    solid_click(pos_open.x, pos_open.y)

                    print("-> Giữ chuột bên Chrome 5s...")
                    pyautogui.moveTo(250, 300, duration=0.4)
                    time.sleep(3)

                    # Quay lại chờ Verify sáng vô hạn thời gian
                    wait_and_click("btn_verify_enabled.png", confidence=0.65, grayscale=False)
                    return True
            except Exception:
                pass

        time.sleep(0.5)

def run_animal_cycle():
    print("\n==========================================")

    # Bước 1: Quét song song Watch Ad & Collect All (Vô hạn thời gian)
    wait_for_watch_ad_or_collect()

    time.sleep(random.uniform(0.2, 0.8))

    # Bước 2: TẮT POPUP TRẮNG OOPS TRƯỚC RỒI BẤM SPONSOR LINK
    print("2. Chờ tắt popup Oops (nút Close)...")
    wait_and_click("btn_close_oops.png", confidence=0.65)
    time.sleep(random.uniform(0.3, 0.8))

    print("-> Bấm 'VISIT SPONSOR LINK & CLAIM'...")
    wait_and_click("btn_visit_sponsor.png", confidence=0.65)
    time.sleep(random.uniform(0.2, 0.8))

    # Bước 3: Bấm Complete Step 2
    print("3. Bấm 'COMPLETE STEP 2 (RICHADS)'...")
    wait_and_click("btn_complete_step2.png", confidence=0.6, grayscale=True)
    time.sleep(random.uniform(0.3, 0.6))

    # Bước 4: Xử lý Verify
    handle_step_verify()
    time.sleep(0.5)

    # Bước 5: Bấm Watch Monetag Final Ad
    print("5. Bấm 'Watch Monetag Final Ad'...")
    wait_and_click("btn_monetag_final.png", confidence=0.6, grayscale=True)

    # Bước 6: Chờ quảng cáo Monetag 16 giây rồi bấm X xanh lá
    print("6. Chờ xem quảng cáo Monetag 16 giây...")
    time.sleep(16)

    print("-> Bấm nút 'final_close' (X màu xanh lá)...")
    wait_and_click("final_close.png", confidence=0.75, grayscale=False)
    time.sleep(random.uniform(0.5, 0.8))

    # Bước 7: Tắt thông báo thành công và bấm Let's Go
    print("7. Tắt popup thành công và bấm 'Let's Go'...")
    check_and_click_if_exists("btn_close_success.png")
    wait_and_click("btn_lets_go.png", confidence=0.65)
    time.sleep(random.uniform(0.5, 0.8))

    # Bước 8: Thu hoạch
    print("8. Thu hoạch phần thưởng...")
    wait_and_click("btn_collect_all.png", confidence=0.7, grayscale=False)
    print("--- HOÀN THÀNH 1 LƯỢT THU HOẠCH ---")
    return True

# --- BẮT ĐẦU CHẠY ---
print("Bot sẽ chạy sau 5 giây. Hãy mở sẵn màn hình game!")
time.sleep(5)

cycle_count = 0

while True:
    try:
        success = run_animal_cycle()
        if success:
            cycle_count += 1
            print(f">> Tổng số lượt hoàn thành: {cycle_count}")
            clean_chrome_tabs()

        time.sleep(random.uniform(1, 2))

    except KeyboardInterrupt:
        print("\nĐã dừng bot an toàn.")
        break