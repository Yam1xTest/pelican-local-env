# Локальная Kubernetes среда  

Более подробную информацию о проекте и связанных с ним репозиториях можно найти здесь:
[pelican-documentation](https://github.com/TourmalineCore/pelican-documentation).

## Подготовка перед запуском

1. Установите Docker
2. Установите Visual Studio Code
3. Установите плагин Visual Studio Code [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Установите [Lens (commercial)](https://k8slens.dev/) или [OpenLens (open source)](https://github.com/MuhammedKalkan/OpenLens/releases)

## VSCode Dev Container

Откройте папку этого репозитория в VSCode, он может сразу предложить вам повторно открыть его в Dev container, или вы можете нажать `Remote Explorer`, найти кнопку плюс и выбрать опцию `Open Current Folder in Container` и подождать пока он будет готов.

Когда Dev Container будет готов, VSCode снова откроется. Откройте новый терминал, который будет выполнять команды в подготовленном Linux-контейнере, который мы уже предварительно установили и настроили:

- Docker Outside of Docker или Docker из Docker, чтобы иметь возможность использовать docker демон хоста изнутри контейнера
- [kind](https://kind.sigs.k8s.io/) для создания локального кластера k8s в Docker
- [kubectl](https://kubernetes.io/docs/reference/kubectl/) для вызова кластера k8s из CLI (в обход Lens)
- [helm, helmfile](https://github.com/helmfile/helmfile) для одновременного развертывания всех сервисов [helm](https://helm.sh/)  в локальном кластере k8s, созданном с помощью `kind`
- [helm-diff](https://github.com/databus23/helm-diff) наглядно показывает, что изменилось с момента последнего применения `helmfile apply`

>Примечание: Вам не нужно устанавливать эти пакеты в свою ОС, они уже являются частью Dev container. Таким образом, это простой способ запустить приложение на любой ОС.

## Управление локальным кластером k8s

### Создание кластера

Чтобы создать новый кластер, в котором вы будете работать, выполните следующую команду **один раз**:

```bash
kind create cluster --name pelican --config kind-local-config.yaml --kubeconfig ./.pelican-cluster-kubeconfig
```

### Удаление кластера

Чтобы удалить ранее созданный кластер, выполните следующую команду:

```bash
kind delete cluster --name pelican
```

### Подключение к кластеру
Затем у вас должна быть возможность получить созданную конфигурацию кластера k8s здесь, в корне репозитория 
`.pelican-cluster-kubeconfig`, и использовать ее в `Lens` для подключения к кластеру.

В `Lens` вы можете перейти в `File` -> `Add Cluster`, поместить туда скопированное содержимое файла `config`.
После чего вы сможете подключиться к нему.

### Развертывание в кластере

Чтобы развернуть приложение в кластере в первый раз или для повторного развертывания после изменения helm-чартов или их конфигурации, выполните следующую команду:

```bash
helmfile cache cleanup && helmfile --environment local --namespace local -f deploy/helmfile.yaml apply
```

Когда команда будет выполнена и все модули k8s будут запущены во вкладке **`local`**, вы сможете перейти по ссылке http://localhost:40110/ в вашем браузере и увидеть `Hello World`.

>Примечание: в первый раз это можеть занять довольно большое количество времени.

>Примечание: `helmfile cache cleanup` необходима для принудительного повторного извлечения values.yaml файлов из репозиториев git. В противном случае это никогда не приведет к их аннулированию.
Ссылки: https://github.com/roboll/helmfile/issues/720#issuecomment-1516613493 и https://helmfile.readthedocs.io/en/latest/#cache.

>Примечание: если была обновлена версия одного из ваших сервисов, например, была опубликована более новая версия `pelican-ui:latest`, вы не увидите изменений, выполнив команду `helmfile apply`. Вместо этого вам нужно удалить соответствующий служебный pod, в случае `pelican-ui` это `pelican-nginx`. После чего он повторно автоматически развернется и получит последние изменения.

### Отладка Helm-чартов

Чтобы увидеть, как будут выглядеть все чарт-манифесты перед применением, вы можете выполнить следующую команду:

```bash
helmfile cache cleanup && helmfile --environment local --namespace local -f deploy/helmfile.yaml template
```

## URLs всех сервисов

- ui: http://localhost:40110
- cms: http://localhost:40110/cms/admin
- minio-s3-ui: http://minio-s3-console.localhost:40110

## Открытие интерфейса minio-s3
- Открыть http://minio-s3-console.localhost:40110
- Ввести логин и пароль:
    - `login`: *admin*
    - `password`: *rootPassword*

## Открытие интерфейса админской панели CMS
- Открыть http://localhost:40110/cms/admin
- Ввести логин и пароль:
    - `email`: *admin@init-strapi-admin.strapi.io*
    - `password`: *admin*

## Возможные проблемы
- OpenLens не показывает никаких развернутых модулей. Убедитесь, что для параметра "Namespace" в поле "Workloads" задано значение "`local`" или "`All namespaces`".

- не открывается http://localhost:40110/
    ```
    Невозможно получить доступ до сайта, локальный хост отказался подключаться.
    ```
    Если вы видите это в своем браузере, пожалуйста, попробуйте открыть сайт в режиме инкогнито.
- не устанавливается чарт pelican-ui
    ```
    COMBINED OUTPUT:
    Release "pelican-ui" does not exist. Installing it now.
    coalesce.go:286: warning: cannot overwrite table with non table for nginx.ingress.annotations (map[])
    coalesce.go:286: warning: cannot overwrite table with non table for nginx.ingress.annotations (map[])
    Error: context deadline exceeded
    ```
    Eсли вы увидите это после попытки выполнить команду `helmfile apply`, просто повторите попытку `helmfile apply`.

- в случае возникновения какой-либо другой странной проблемы:
    1. Удалите docker container под названием `pelican-control-plane`.
    2. Удалите кластер из Lens.
    3. Попробуйте выполнить все команды из инструкции, начиная с `kind create`.

## Полезные ссылки, используемые для настройки репозитория

- https://shisho.dev/blog/posts/docker-in-docker/
- https://devopscube.com/run-docker-in-docker/
- https://github.com/kubernetes-sigs/kind/issues/3196
- https://github.com/devcontainers/features
- https://fenyuk.medium.com/helm-for-kubernetes-helmfile-c22d1ab5e604
