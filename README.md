# product-sales_service
관리자가 상품을 등록하고 유저가 상품을 사는 서비스
# what_university_user_like

가상의 마켓 API 구현

  <details>
  <summary>가상의 결제를 위한 포인트 시스템</summary>
  <div markdown="1">
  
  #### 결제 시스템 준비를 위한 User에 포인트 충전 요소 구현!<br>
  ```python
  
    def charge_point(point_data, user):
      user.point = user.point + int(point_data["point"])
      user.save()
      return point_data["point"], user.point
    
    
    class ChargePointView(APIView):
      """
      유저가 포인트를 충전하는 View
      """

      def post(self, request):
          user = request.user
          before_point, cur_point = charge_point(request.data, user)
          return Response({"detail": (user.username + "님의 포인트가 " + str(before_point) + "포인트가 충전되어서" + str(cur_point) + "포인트가 되셨습니다.")}, status=status.HTTP_200_OK)

  ```
  </div>
  </details>
  <details>
  <summary>permission을 함수로 구현</summary>
  <div markdown="1">
  
  #### Service Layer에서 권한 체크, 결제 가능 여부 체크 로직 작성!<br>
  #### But, Permission을 사용하는 것이 바람직하지 않았나 하는 스스로의 피드백. <br>
  
  ```python
   
    def check_is_admin(user: User) -> bool:
      """
      현재 서비스를이용하는 유저가 관리자인지를 체크하는 service
      Args:
          user (User): 로그인한 User_obj
      Returns:
          bool: 관리자라면 True, 일반유저라면 False
      """
      if user.is_admin == True:
          return True
      return False
      
      
    def check_user_can_pay(total_price: int, user: User) -> bool:
      """
      유저가 결제할 수 있는 포인트를 지녔는가를 확인하는 service
      Args:
          total_price (int): 유저가 결제를 해야하는 포인트
          user (User): 로그인이 되어있는 user_obj
      Returns:
          bool: 결제할 포인트가 있다면 True
                결제할 포인트가 없다면 False
      """
      if user.point >= total_price:
          return True
      return False
      `
      `
      `
  ```
  </div>
  </details>
  <details>
  <summary>결제가 가능한 포인트가 있고, 포인트를 통한 결제가 이루어졌을 경우 결제 내역 작성</summary>
  <div markdown="1">
  
  #### 결제의 영수증 역할을 함.<br>
  #### 결재금액, 잔액 등등을 기입하여 나중에 환불을 할 때에도 활용이 가능함.<br>
  ```python
  def create_pay_history(pay_data: dict, user: User, product_id: int, balance_point: int, total_price: int) -> None:
    """
    결제가 진행된 후, 결제내역을 생성해주는 Service
    Args:
        pay_data (dict): {
            count (int) : 결제할 상품의 수량
        }
        user (User): 로그인한 user_obj,
        product_id (int): 결제하려는 상품의 id,
        balance_point (int): 결제하고 난 뒤의 잔액 포인트
        total_price (int): 결제하려는 총 금액
    """
    pay_data["user"] = user.id
    pay_data["product"] = product_id
    pay_data["balance"] = balance_point
    pay_data["total_price"] = total_price
    pay_history_serializer = PayHistorySerializer(data=pay_data)
    pay_history_serializer.is_valid(raise_exception=True)
    pay_history_serializer.save()
  ```
  </div>
  </details>
  <details>
  <summary>결제 내역을 토대로 환불을 해주는 로직</summary>
  <div markdown="1">
  
  #### 결제 내역을 토대로 결제를 취소한 후 영수증의 금액대로 포인트를 재 지급<br>
  ```python
    
  def refund_product(pay_history_id: int):
    """
    결제내역을 토대로 환불을 진행하는 service
    Args:
        pay_history_id (int): _description_
    """
    pay_history_obj = PayHistoryModel.objects.get(id=pay_history_id)
    user = pay_history_obj.user
    user.point = int(user.point) + int(pay_history_obj.total_price)
    pay_history_obj.delete()
    user.save()

    return pay_history_obj.total_price, user.point
  ```
  </div>
  </details>

## 👉 ERD

![image](https://user-images.githubusercontent.com/101394490/190910621-c492551d-df60-4f3c-95df-468cebd6a395.png)


## 📌 컨벤션

### ❓ Commit Message

- feat/ : 새로운 기능 추가/수정/삭제
- enhan/ : 기존 코드에 기능을 추가하거나 기능을 강화할 때
- refac/ : 코드 리팩토링,버그 수정
- test/ : 테스트 코드/기능 추가
- edit/ : 파일을 수정한 경우(파일위치변경, 파일이름 변경, 삭제)

### ❓ Naming

- Class : Pascal
- Variable : Snake
- Function : Snake
- Constant : Pascal + Snake

### ❓ 주석

- Docstring을 활용하여 클래스와 함수단위에 설명을 적어주도록 하자.
- input/output을 명시하여 문서 없이 코드만으로 어떠한 결과가 나오는지 알 수 있도록 하자.

