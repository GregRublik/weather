В основе лежит flask. Я пишу на нем в первый раз если честно решил попробовать. 
Для бд использую postgresql, а для работы с ней sqlalchemy. Небольшой скрипт для ajax запросов



По заданию выполнено:
- сделаны автодополнение (подсказки) при вводе города
- при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
- будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город

Я попытался создать докер контейнер, но я не успел так как мне дополнительно нужно подключить бд к контейнеру

# Для запуска требуется:
    ## установить python 
    ## установить requirements.txt
    ## установить переменные окружения в файле .env и создать db в postgresql
    ## запустить main.py