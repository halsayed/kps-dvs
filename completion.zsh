#compdef kps

_arguments \
  '1: :->level1' \
  '2: :->level2' \
  '3: :_files'
case $state in
  level1)
    case $words[1] in
      kps)
        _arguments '1: :(completion config create debug delete get help log service update)'
      ;;
      *)
        _arguments '*: :_files'
      ;;
    esac
  ;;
  level2)
    case $words[2] in
      log)
        _arguments '2: :(app pipeline)'
      ;;
      service)
        _arguments '2: :(disable enable)'
      ;;
      update)
        _arguments '2: :(svcdomain)'
      ;;
      completion)
        _arguments '2: :(bash zsh)'
      ;;
      config)
        _arguments '2: :(create-context delete-context get-contexts use-context)'
      ;;
      debug)
        _arguments '2: :(function pipeline purge)'
      ;;
      delete)
        _arguments '2: :(application category datapipeline datasource function logcollector service)'
      ;;
      get)
        _arguments '2: :(application category datapipeline datasource function logcollector node project service svcdomain)'
      ;;
      *)
        _arguments '*: :_files'
      ;;
    esac
  ;;
  *)
    _arguments '*: :_files'
  ;;
esac
