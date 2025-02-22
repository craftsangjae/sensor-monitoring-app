## Loki / Grafana / Prometheus / Tempo 설치하기

### 1. [로키 설치](https://grafana.com/docs/loki/latest/setup/install/helm/install-scalable/)

````shell
helm repo add grafana https://grafana.github.io/helm-charts

helm repo update

helm install loki grafana/loki -n monitoring -f loki-values.yaml
````

* loki-values 중요 포인트들

1. 모드 설정: SimpleScalable로 지정
2. 레플리카 수 설정: 1로 지정
3. nodeSelector 설정: node-role: monitoring으로 지정
4. 인덱스 설정: 24h로 지정
5. 청크 인코딩 설정: snappy로 지정

### 2. [Promtail 설치](https://grafana.com/docs/loki/latest/setup/install/helm/install-promtail/)

````shell
helm install promtail grafana/promtail -n monitoring -f promtail-values.yaml
````

* promtail-values 중요 포인트들

1. 파서 설정:
````yaml
snippets:
pipelineStages:
    - cri: {} 

    - json:
        expressions:
        timestamp: timestamp
        level: level
        trace_id: trace_id
        span_id: span_id
        name: name
        method: method
        message: message
````

### 3. [Prometheus 설치]

````shell 
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
````

````shell
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring -f prometheus-stack-values.yaml
````

* prometheus-stack-values 중요 포인트들

1. `serviceMonitorSelectorNilUsesHelmValues`: false 로 변경해서 ServiceMonitor 스크래핑 전역적으로 가능하도록
2. `nodeSelector`: node-role: monitoring으로 지정
3. `grafana.enabled`: false로 지정
4. `alertmanager.enabled`: false로 지정

### 4. [Grafana 설치](https://grafana.com/docs/grafana/latest/setup-grafana/installation/helm/)

````shell
helm install grafana grafana/grafana -n monitoring -f grafana-values.yaml
````

* grafana-values 중요 포인트들

1. 로그인 설정
````yaml
adminUser: admin
adminPassword: sksmsqkseltqnf
````

2. 노드 선택자 설정
````yaml
nodeSelector:
    node-role: monitoring
````
