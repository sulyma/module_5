import hashlib
import time


class UrTube:

    def __init__(self, *videos):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        for user in self.users:
            if user.nickname == nickname and user.password == hashlib.md5(password.encode()).hexdigest():
                self.current_user = user
                print(f'Пользователь {nickname} вошел в систему.')
                return
        print('Неверный логин или пароль.')

    def add(self, *video_obj):
        for video in video_obj:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)

    def register(self, nickname, password, age):
        for user in self.users:
            if user.nickname == nickname:
                print(f'Пользователь {nickname} уже существует')
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    def log_out(self):
        print(f'Пользователь {self.current_user} вышел из системы.')
        self.current_user = None

    def get_videos(self, search_term):
        return [video.title for video in self.videos if search_term.lower() in video.title.lower()]

    def watch_video(self, title):
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста, покиньте страницу")
                    return

                while video.time_now < video.duration:
                    print(f'Секунда: {video.time_now}')
                    time.sleep(1)
                    video.time_now += 1

                print("Конец видео")
                video.time_now = 0  # сбрасываем текущее время просмотра
                return

        print("Видео не найдено.")


class Video:
    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.age = age

    def __str__(self):
        return f'{self.nickname}'


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')