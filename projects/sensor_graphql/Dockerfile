# Node.js 공식 이미지를 베이스로 사용
FROM node:18-slim

# 작업 디렉토리 생성
WORKDIR /app

# package.json과 package-lock.json을 먼저 복사
COPY package*.json ./

# 의존성 설치
RUN npm install

# 소스 코드 복사
COPY plugins/ plugins/
COPY index.js index.js

# 포트 3000 노출
EXPOSE 3000

# 애플리케이션 실행
CMD ["node", "index.js"]