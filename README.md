# boj-tool
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/sohnryang/boj-tool/pulls)
![Python 3](https://img.shields.io/badge/python-3-blue.svg)
[![PyPI downloads](https://img.shields.io/badge/dynamic/json.svg?label=downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fboj-tool%2Foverall&query=%24.data%5B0%5D.downloads&colorB=blue&suffix=%20overall)](https://pypi.org/project/boj-tool/)
[![GitHub license](https://img.shields.io/github/license/sohnryang/boj-tool.svg)](https://github.com/sohnryang/boj-tool/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/sohnryang/boj-tool.svg)](https://github.com/sohnryang/boj-tool/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sohnryang/boj-tool.svg)](https://github.com/sohnryang/boj-tool/network)
[![GitHub issues](https://img.shields.io/github/issues/sohnryang/boj-tool.svg)](https://github.com/sohnryang/boj-tool/issues)

## tl;dr 설치/사용 방법

### 설치
[PyPI](https://pypi.org/project/boj-tool/)에 올라와 있기 때문에 간단히 설치할 수 있다.
```
pip install boj-tool
```

### 사용법

#### 로그인
```
boj login
```

#### 제출
```
boj submit [문제 번호] [제출할 코드 경로]
```

#### 전적 조회
- 자신의 전적을 조회하는 경우
```
boj stats
```
- 다른 사림의 전적을 조회하는 경우
```
boj stats --user [유저 이름]
```

## 무엇인가?
[백준 온라인 저지](https://www.acmicpc.net)에 코드를 자동으로 제출하는 도구이다. 하지만 이름이 `boj-tool`인 것은 그 외에도 더 많은 기능을 지원할 예정이기 때문이다.

[BOJ API](https://www.acmicpc.net/board/view/10929)가 만들어지면 그것을 이용해 더 많은 기능을 추가할 예정이다.

## 왜 만들었는가?
- 커맨드 라인을 많이 사용하는 내 workflow 특성상 CLI tool이 편하다.
- [기존에 있던](https://github.com/sjy366/BOJ-Auto-Submit) [도구들](https://github.com/Baekjoon/submit-tool)이 내가 원하는 것과 미세하게 달랐다.
- 뭔가 코딩하고 싶었다.
- 과고 떨어져서 스트레스를 풀고 싶었다.

## 지원 언어
> 참고: 이 리스트에 없는 언어가 없으면 [Issue](https://github.com/sohnryang/boj-tool/issues)를 만들거나 [PR](https://github.com/sohnryang/boj-tool/pulls)을 보내면 지원 추가 예정이다.

- C++ (Clang, C++14, C++17 등 모두 지원)
- C (Clang, C11 등 모두 지원)
- Python (2, 3, pypy 등 모두 지원)
- Java (Oracle Java와 OpenJDK 모두 지원)
- JavaScript
- Text
- 아희

## 기능
- 쿠키를 이용한 로그인 정보 저장 (컴퓨터에 ID/Password가 저장되지 않는다.)
- 설정 파일을 통한 언어의 컴파일러, 버전 지정
- 디버깅을 위한 로깅 기능

## Roadmap
- [ ] 리팩터링
- [x] 전적 조회 기능
- [ ] 모든 언어 지원 (꼭 할것은 아님)

## 라이선스
[MIT 라이선스](https://github.com/sohnryang/boj-tool/blob/master/LICENSE)
