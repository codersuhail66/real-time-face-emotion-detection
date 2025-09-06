import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # or try CAP_MSMF
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera not accessible")
        break
    cv2.imshow("Test Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
