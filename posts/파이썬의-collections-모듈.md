# 파이썬의 Counter

📅 2025-07-04T08:23:54.038Z

🔗 [원문 링크](https://velog.io/@son-dan-ha/파이썬의-collections-모듈)

---

# `collections` 모듈
collections 모듈에는 컬렉션(자료구조) 클래스가 들어있다. 잘 알아두면 코드를 짧고 간결하게 구현할 수 있다.

컬렉션 모듈이 제공하는 클래스는 다음과 같다. 

1. Counter
2. deque
3. defaultdict
4. OrderedDict
5. namedtuple

오늘은 이 중 Counter를 알아보겠다. 
<br>

---

# `Counter`

Counter는 **딕셔너리의 서브 클래스**이다. 따라서 딕셔너리의 특징을 가지고 있다. 파이썬 3.7 부터 딕셔너리는 순서를 갖고 Counter 또한 마찬가지다.

<br><br>

## `Counter`의 기본 기능

Counter는 각 요소의 **등장 횟수**를 자동으로 세어주는 딕셔너리 기반 클래스다. 존재하지 않는 key를 조회하면 KeyError 대신 0을 반환한다.

<br>

- `Counter(iterable)`  
  이터러블의 각 요소를 key로, 등장 횟수를 value로 저장한다.

- `most_common(n)`  
  가장 많이 등장한 요소부터 `(key, count)` 형태로 반환한다.  
  n을 생략하면 전체를 빈도순으로 반환한다.

- `total()`  
  모든 value의 합을 반환한다.  
  즉, Counter에 저장된 전체 요소 개수를 의미한다.

- `subtract(other)`  
  다른 Counter나 이터러블을 인자로 받아 값을 **감소**시킨다.  
  뺄셈(`-`)과 달리 0 이하의 값도 유지된다.

- `update(other)`  
  다른 Counter나 이터러블을 받아 값을 **누적**한다.


<br><br>

## `Counter`의 산술연산
[완주하지 못한 선수](https://school.programmers.co.kr/learn/courses/30/lessons/42576)

> Key-value쌍으로 데이터를 찾는 해시 알고리즘 문제다. 해당 문제에서는 총 선수의 이름이 담긴 배열과 완주한 선수의 이름이 담긴 배열을 준다. 이름에는 중복된 값이 있을 수 있다. 

<br>

**Counter의 뺄셈**으로 문제를 해결해보았다. 

<br>

```python
from collections import Counter 

def solution(participant, completion):
    return list((Counter(participant)-Counter(completion)).keys())[0]
````

**슬라이싱**은 리스트의 메서드이므로 **list로 형변환**을 한 후 0번 인덱스를 추출하였다.

<br>

**리스트**를 사용하여 답을 구할 수도 있다. 아래는 딕셔너리를 사용하지 않고 리스트로 값을 하나하나 비교한 풀이다.

```python
def solution(participant, completion):
    
    sorted_p = sorted(participant)
    sorted_c = sorted(completion)
        
    for idx, c in enumerate(sorted_c):
        if c != sorted_p[idx] and c == sorted_p[idx+1]:
            return sorted_p[idx]
        
    return sorted_p[-1]
```

<br>

## `Counter`의 `elements()`

collections.Counter의 `.elements()`는 각 **요소**를 그 **개수만큼 반복**하여 반환하는 이터레이터(iterator)이다. 따라서 list(), sorted(), set() 등 **이터러블을 받는 함수**에서 사용 가능하다.

<br>

[숫자 짝꿍](https://school.programmers.co.kr/learn/courses/30/lessons/131128)

<br>

아래는 `elements()`를 사용한 풀이 코드다.

```python
from collections import Counter

def solution(X, Y):
    x, y = Counter(X), Counter(Y)

    cnt = Counter()
    for i in range(10):
        if x[str(i)] * y[str(i)] != 0:
            cnt[str(i)] = min(x[str(i)], y[str(i)])
    
    if not cnt:
        return "-1"
    else:
        answer = ''.join(sorted(cnt.elements(), reverse=True))
        if int(answer) == 0:
            return "0"
        else:
            return answer
```

다음 코드는 테스트에서 **시간 초과**가 났다. 그 이유는 elements() 연산의 **시간복잡도**에 있었다.

<br>

### `elements()`의 시간복잡도

연산이 오래 걸리는 코드
`answer = ''.join(sorted(cnt.elements(), reverse=True))`

> 앞서 elements()는 각 요소를 그 개수만큼 반복한다.
> 전체 원소 개수를 K라고 하면 `cnt.elements()`는 O(K)의 시간복잡도를 갖고,
> 이후 `sorted()`에서 O(K log K)의 정렬 연산이 수행된다.

* 총 시간복잡도 = **O(K log K)**

<br>

### `String`의 시간복잡도

아래처럼 elements()를 사용하지 않고 빈 **문자열**에 값을 **누적**하는 방식으로 수정했지만 여전히 **시간 초과**가 났다.

```python
answer = ''
for i in range(9, -1, -1):
    answer += (str(i) * cnt[str(i)])
```

**파이썬의 문자열**은 **불변(immutable)**하다.

위 처럼 문자열에 n번 반복하여 값을 추가한다면
매 연산마다 기존 문자열을 복사하므로 시간복잡도는 **O(n²)**가 된다.

<br>

### 개선된 코드

위에서 실패한 원인들을 바탕으로 `''.join()`만을 사용한 코드를 작성한 결과 통과했다.
아래 코드는 문자열을 직접 누적하지 않고, 문자열 조각을 모은 뒤 `''.join()`으로 한 번만 문자열을 생성했기 때문에 효율적으로 동작한다.

<br>

---

# reference

[Python-collections](https://docs.python.org/ko/3.13/library/collections.html#collections.Counter)


