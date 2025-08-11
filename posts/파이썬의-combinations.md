# 파이썬의 combinations

📅 2025-08-11T06:53:40.774Z

🔗 [원문 링크](https://velog.io/@son-dan-ha/파이썬의-combinations)

---


>해시 알고리즘에 속하는 [의상](https://school.programmers.co.kr/learn/courses/30/lessons/42578) 문제를 해결하는 과정이다. 이 문제를 통해 파이썬의 3가지 모듈을 새롭게 알게 되었다. 또한 조합 원리로 문제를 해결하는 아이디어를 얻을 수 있었다. 
이 포스트는 조합 아이디어에 대한 간단한 정리와 파이썬의 모듈에서 combinations(), reduce(), mul의 활용 방법과 내부 동작 원리를 알아본다.

<br>


# 문제 풀이

해당 문제는 조합을 구하는 문제라고 생각했다. 따라서 주어진 매개변수를 Counter를 활용해 가공 후 **조합을 구현**하려고 했다. 그러나 조합 구현에는 제어 흐름과 인덱스를 증가하고 정렬하는 것이 중요하다. 완벽하게 구현하는 데에는 어려움이 있으므로 이미 만들어진 모듈을 활용하는 것은 에러 없는 코드를 작성하기 위한 좋은 방법이라 생각한다.

<br>

## 내가 작성한 풀이

문제 **조건에 맞는 모든 경우**를 찾아내는 것이 목적이었다. 그러나 많은 케이스에서 정답을 내지 못했다. 

```python
from collections import Counter
from functools import reduce

def solution(clothes):
    answer = 0
    values = list(Counter([i[1] for i in clothes]).values())
    N = len(values)
    
    # 조합을 직접 구현하려 함 -> 다양한 문제점
    for i in range(1,N+1):
    
        # 문제에만 맞춘 분기로 인해 확장성과 가독성 떨어짐
        if i == 1: 
            answer+= sum(values)
            
        elif i == 2: # 2C2, 3C2, 4C2
            for idx, v in enumerate(values):
                n = idx +1
                while n <= N-1:
                    answer += v*values[n]
                    n += 1
                    
        elif i == 3: 
            if N == 3: # 3C3
            	# 람다 사용으로 가독성이 떨어짐
                answer += reduce(lambda x,y:x*y, values)
            
            elif N == 4: # 4C3
                for i in range(N):
                    l = values # 얉은 복사 -> 원본 훼손
                    l.pop(i)
                    answer += reduce(lambda x,y:x*y, l)
        
        elif i == 4: # 4C4
            answer += reduce(lambda x,y:x*y, values)

    return answer
```

<br>

## 모듈을 활용한 풀이

조합을 구현하려 했던 코드는 많은 **논리적 오류**와 **문법적 오류**를 가지고 있다. 따라서 **조합 모듈**을 사용한 위와 같은 구조의 개선된 코드를 찾아 보았다.

```python
from collections import Counter
from itertools import combinations
from functools import reduce 
from operator import mul # lambda 대신 사용 

def solution(clothes):
    answer = 0
    values = list(Counter([i[1] for i in clothes]).values())
    N = len(values)

    # 모듈을 통해 조합 함수를 사용
    for r in range(1, N + 1):
    	# combinations(이터러블한 객체, r개 조합)
        # comb는 r개 종류를 선택하는 조합의 경우
        for comb in combinations(values, r):
            answer += reduce(mul, comb)
    
    return answer
```

itertools 모듈의 combinations 함수를 사용했더니 복잡했던 코드가 간결하게 정리되었다. 다만 해당 코드는 시간복잡도에 걸렸다. 내가 위에서 작성한 코드의 구성과 똑같이 조합을 **1개부터 N개까지 모두 구해서 곱을 누적하는 방식**이다. 조합의 경우는 N이 늘어날 수록 그 결과 값이 급격하게 증가한다. 이는 코드가 동작할 때 연산량의 증가로 이어진다. 


### 조합의 시간복잡도
$\sum_{r=1}^{N}(_nC_r)\times{r}=O(2^N\cdot{N})$

<br>

## 조합 원리를 활용한 풀이

문제를 해결하는 아이디어가 중요했다. 조합을 구하는 공식을 사용할 경우 위처럼 증가하는 연산량으로 인해 **시간복잡도에서 문제**가 생겼다. 

문제를 다시 살펴보면 **거의 모든 경우**를 구하지만 아무것도 선택하지 않는 경우(의상을 한개도 선택하지 않는 경우)는 **제외**한다. 

많은 경우가 예상될 때 제외하는 조건이 구하기 쉬운 경우(전체 경우보다 훨씬 적은 경우)에는 **여사건**을 이용할 수 있다.

### 여사건

여사건은 어떤 사건이 일어나지 않을 경우를 말한다. 간단하게 개념을 설명하면 표본공간이 S 일때, 여사건 $\overline{A}$는 다음과 같다. 

$$\overline{A}=S−A$$

이를 문제에 적용 시키면, 전체 경우의 수는 0개를 선택하는 경우부터 전체를 하나씩 선택하는 경우다. 

따라서 종류가 n개 있을 때, 각 종류마다의 개수를 $X_i$라고 한다면, 
- 전체 경우의 수 = $(x_1+1)\times(x_2+1)···(x_i+1)···(x_n-1+1)\times(x_n+1)$
- 해당 종류를 선택하지 않는 경우 (+1) + 선택하는 경우($X$)

여기서 여사건은 모든 종류를 선택하지 않는 경우 1가지로 최종 경우의 수는 

$\sum_{i=1}^{n}(x_i+1)-1$

<br>

코드로는`reduce(mul,[i+1 for i in values])` 처럼 작성 가능하다. 곱의 법칙을 이용하므로 mul 함수를 사용하였는데, lambda를 사용하여 `reduce(lambda x,y: x*y,[i+1 for i in values])` 처럼 작성할 수도 있다.

### 최종 코드

```python
from collections import Counter
from functools import reduce
from operator import mul  

def solution(clothes):
    # 의상 종류별 개수 세기
    values = list(Counter([i[1] for i in clothes]).values())

    # 여사건 계산: 전체 경우의 수 - 아무것도 안입는 경우    
    return reduce(mul,[i+1 for i in values]) - 1
```




<br>
<br>

---

# `combinations()`

조합을 직접 활용하려고 했을 때, 시간 초과가 났다. 고등교육 과정에서의 조합까지만 알고 있기에 파이썬에서 구현된 조합은 어떤 구조일지 알아보자. 

<br>

combinations은 itertools 안에 들어있다. 

`from itertools import combinations` 

따라서 파이썬에서 조합을 사용하기 위해서는 다음과 같이 모듈을 가져온다.


## itertools
조합은 `itertools` 모듈에 포함되어 있다. itertools 모듈은 이름 그대로 iterable한 객체에서 사용할 수 있는 도구(함수)를 제공한다. 특히 반복되는 계산에서 유용하게 사용 가능하다. itertools의 모든 함수는 lazy evaluation(지연 평가)를 사용한다. 

<br> 

combinations 외의 itertools의 함수 몇가지
- `itertools.count(start=0, step=1)` : 증가하는 값을 무한히 생성
- `itertools.cycle(iterable)` : 순서대로 무한히 반복 ( [1,2,3] -> 1,2,3,1,2,3,1 ... )
- `itertools.repeat(object[, times])`
- `itertools.chain(*iterables)` : 이터러블하면, 자료형에 관계없이 모두 연결

<br> 

### lazy evaluation

지연 평가란 **필요할 때마다** 값을 계산하는 이터레이터를 반환한다는 의미다. 파이썬에서 이터레이터나 제너레이터와 같은 객체들은 지연 평가 방식을 따른다. 이 방식은 메모리 사용과 계산 비용을 줄인다. `next()` 함수가 호출될 때마다 하나씩 계산하여 반환하는 구조를 갖는다. 

<br> 

## 동작 원리

> 참고: 앞으로의 파이썬 내부 동작 원리는 CPython 기준으로 작성됨.
- 컴파일: `.py` -> `.pyc`
- 실행 방식: 바이트코드 인터프리터(C로 작성)가 한 줄씩 실행

<br>

`itertools`는 **C**로 구현되어 있다. 아래 예시는 공식 문서에서 제공하는 파이썬으로 작성한 개념적 **유사 코드**로, 실제 구현은 아니다.

```python
def combinations(iterable, r):
    pool = tuple(iterable) # 이터레이터를 입력받아 튜플로 저장
    n = len(pool) 
    
    if r > n: # 조합을 구할 수 없는 경우
        return
        
    indices = list(range(r)) # 인덱스 리스트 생성
    
    # 첫번째 조합 반환
    yield tuple(pool[i] for i in indices)
    
    while True: # 조합 모두 찾기
        
        for i in reversed(range(r)): 
        	# 다음 조합을 생성할 수 있다면 계속 (while 종료 x)
            if indices[i] != i + n - r: 
                break 
                
        else: # break 없이 정상적으로 끝났을 경우 (for-else)
        	return # 조합 찾기 끝
         
        indices[i] += 1
        
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
            
        # 지연 평가 방식으로 조합 튜플 반환    
        yield tuple(pool[i] for i in indices)
```

### yield와 return 

- `return`은 함수를 **종료**하고 **값을 반환**한다. 
- `yield`는 함수가 **종료되지 않고** 상태를 유지하며, 여러 값을 순차적으로 반환하며 최종 값은 **제너레이터 객체**가 된다. `next()` 호출로 **값을 하나씩 전달**하게 된다.


<br>

---

# `reduce()`

`from functools import reduce`

reduce은 functools 안에 들어있다. functools 모듈은 **고차 함수** 및 **함수형 도구**들을 제공한다. 

`functools.reduce(function, iterable[, initializer])`

reduce는 function에 대해서 iterable에 누적 적용할 수 있게 한다. 문제에서는 리스트 내의 요소를 차례로 곱하여 누적하는 연산을 진행했다. 

>`reduce(mul, [5, 3, 6, 8])`
리스트에서 5와 3을 꺼내 mul 함수에 적용. → $5\times3$
리스트에서 다음 값 6을 꺼내 앞 연산에서 mul 함수를 적용함 (곱을 누적) → $5\times3\times6$
이를 계속 반복 → $5\times3\times6\times8$
return 되는 값은 `5*3*6*8`




<br>

---

# `mul`

`from operator import mul`

mul은 operator 안에 들어있다. operator 모듈은 파이썬의 **내장 연산자를 함수 형태**로 제공한다. 보통 함수의 이름은 특수 메서드에서 앞뒤 밑줄을 뺀 형태를 갖는다. 

- 산술/수학 연산자 : `add`, `sub`, `mul`, ...
- 비트 연산자 : `and_`, `or_`, `xor`, ...
- 논리/비교 : `lt`, `le`, `eq`, ...
- ...

해당 모듈의 특징은 내장 연산자를 함수 형태로 제공하므로 `operator.mul`은 **내장 곱셈 연산**을 그대로 **호출**하는 wrapper로 이해하면 된다.

## 동작 원리

### 메서드 디스패치

메서드가 호출될 때 실제로 실행될 메서드를 결정하는 과정을 메서드 디스패치라고 한다. 메서드 디스패치에는 컴파일 과정에서 결정되는 **정적 디스패치**와 런타임 과정에서 결정되는 **동적 디스패치**가 있다. 

정적 타입의 언어가 아닌 파이썬은 **런타임**에 피연산자의 **타입을 확인**하고 그 타입이 제공하는 **연산을 찾아 호출**하는 방식을 갖는다. (코드 작성 시점에 타입이 확정되는 것이 아님)

mul은 좌, 우, 제자리 순서로 판단한다. `a*b`를 받는다면 `a.__mul__(b)` 호출하는데, 이때 `NotImplemented`(예외 X) 라면 `b.__rmul__(a)`를 호출하고 둘다 불가능하면 `TypeError`가 난다. 

```python
class Box:
    def __init__(self, v): 
    	# 인스턴스 속성 정의. (단일 숫자만 담음)
    	self.v = v
    
    def __repr__(self):
    	return f"{self.v}"
        
    # a * b  → a.__mul__(b) 
    # 먼저 호출되는 왼쪽 연산자
    def __mul__(self, other): 
        if isinstance(other, (int, float)):
            return Box(self.v * other)
            
        # NotImplemented는 반사 호출 유도에 쓰이는 신호값
        # 인터프리터가 반사 연산(__r*__) 자동 폴백
        # 여기서는 __rmul__
        return NotImplemented 
        
    # 반사 곱: 
    # a * b 에서 a.__mul__(b) 가 NotImplemented
    # → b.__rmul__(a)    
    def __rmul__(self, other): # 우
        if isinstance(other, (int, float)):
            return Box(other * self.v)
        return NotImplemented

	# a *= b  → 우선 a.__imul__(b) 를 시도
    # self 내부 상태를 바꾸고 self 반환
    def __imul__(self, other):            
        if isinstance(other, (int, float)):
            self.v *= other # 제자리 갱신(in-place)
            return self # 제자리 연산은 보통 self를 돌려줌                  
        
        # NotImplemented 반환 
        # → 일반 곱으로 폴백되어 a = a * b 수행
        return NotImplemented
```

```python 
b = Box(10)
print(b * 3) # 30
print(3 * b) # 30

b *= 2
print(b) # 20
```



구조를 보면 알겠지만 사실상 mul 등의 여러 연산 함수는 기본 **내장 함수** `*` 등을 사용하는 것과 **동일**하다. 단지 함수 형태로 호출한다는 특징을 갖는다. 이런 형태의 장점은 성능상의 이득이 아닌 **함수형 유틸과의 결합성**에 있다. 문제에서 활용할 때에도 함수형 도구인 `reduce()` 와 결합되어 사용되었다. **함수형 프로그래밍**에 유용하게 사용될 수 있겠다.

<br>

---

# Reference

- [itertools - combinations](https://docs.python.org/3/library/itertools.html#itertools.combinations)
- [functools - reduce](https://docs.python.org/3/library/functools.html#functools.reduce)
- [operator - mul](https://docs.python.org/3/library/functools.html#functools.reduce)





















