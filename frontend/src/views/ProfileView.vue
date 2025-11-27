<template>
  <div class="h-full overflow-auto p-6 bg-white dark:bg-gray-900">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Профиль</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Profile Card -->
        <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
          <div class="text-center">
            <div v-if="user?.avatar_url" class="w-24 h-24 rounded-full mx-auto mb-4 overflow-hidden">
              <img :src="`http://localhost:8000${user.avatar_url}`" alt="Avatar" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-24 h-24 rounded-full bg-primary-600 flex items-center justify-center text-white text-3xl font-semibold mx-auto mb-4">
              {{ userInitials }}
            </div>
            <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
              {{ user?.first_name }} {{ user?.last_name }}
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">@{{ user?.username }}</p>
            <p class="text-gray-500 dark:text-gray-400 text-sm mt-2">{{ user?.position || 'Сотрудник' }}</p>
            
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleAvatarUpload"
            />
            <button @click="() => avatarInput.click()" class="mt-4 w-full btn-secondary">
              Изменить фото
            </button>
          </div>
        </div>
        
        <!-- Profile Info -->
        <div class="lg:col-span-2 space-y-6">
          <div class="card dark:bg-gray-800 dark:border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Настройки</h3>
            <div class="space-y-3">
              
              <!-- Аккордеон: Основные настройки -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button
                  @click="toggleSection('basic')"
                  class="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <UserCircleIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <span class="font-medium text-gray-900 dark:text-gray-100">Основные настройки</span>
                  </div>
                  <ChevronDownIcon
                    :class="[
                      'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
                      expandedSections.basic ? 'rotate-180' : ''
                    ]"
                  />
                </button>
                <div v-show="expandedSections.basic" class="p-4 space-y-6 bg-white dark:bg-gray-800">
              <!-- Статус -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Статус</label>
                <select
                  v-model="settingsData.status"
                  @change="handleUpdateField('status', settingsData.status)"
                  class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                >
                  <option value="online">🟢 Онлайн</option>
                  <option value="away">🟡 Отошел</option>
                  <option value="offline">⚪ Оффлайн</option>
                </select>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Ваш статус виден другим пользователям
                </p>
              </div>

              <!-- Имя пользователя -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Имя пользователя</label>
                <div class="flex gap-2">
                  <input
                    v-model="settingsData.username"
                    type="text"
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 flex-1"
                    :placeholder="user?.username"
                  />
                  <button
                    @click="handleUpdateField('username', settingsData.username)"
                    class="btn-secondary whitespace-nowrap"
                    :disabled="!settingsData.username || settingsData.username === user?.username"
                  >
                    Изменить
                  </button>
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Уникальное имя для входа в систему
                </p>
              </div>

              <!-- Email -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
                <div class="flex gap-2">
                  <input
                    v-model="settingsData.email"
                    type="email"
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 flex-1"
                    :placeholder="user?.email || 'email@example.com'"
                  />
                  <button
                    @click="handleUpdateField('email', settingsData.email)"
                    class="btn-secondary whitespace-nowrap"
                    :disabled="!settingsData.email || settingsData.email === user?.email"
                  >
                    Изменить
                  </button>
                </div>
              </div>

              <!-- Телефон -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Телефон</label>
                <div class="flex gap-2">
                  <div class="flex items-center flex-1">
                    <span class="px-3 py-2 bg-gray-100 dark:bg-gray-700 border border-r-0 border-gray-300 dark:border-gray-600 rounded-l-lg text-gray-700 dark:text-gray-300">
                      +7
                    </span>
                    <input
                      v-model="settingsData.phone"
                      type="tel"
                      maxlength="9"
                      pattern="[0-9]{9}"
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 rounded-l-none flex-1"
                      :placeholder="getPhoneDisplay(user?.phone) || '912345678'"
                      @input="validateSettingsPhone"
                    />
                  </div>
                  <button
                    @click="handleUpdateField('phone', settingsData.phone ? `+7${settingsData.phone}` : null)"
                    class="btn-secondary whitespace-nowrap"
                    :disabled="settingsPhoneError || (!settingsData.phone && !user?.phone)"
                  >
                    Изменить
                  </button>
                </div>
                <p v-if="settingsPhoneError" class="text-red-600 dark:text-red-400 text-sm mt-1">{{ settingsPhoneError }}</p>
              </div>

              <!-- Должность -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Должность</label>
                <div class="flex gap-2">
                  <input
                    v-model="settingsData.position"
                    type="text"
                    class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 flex-1"
                    :placeholder="user?.position || 'Ваша должность'"
                  />
                  <button
                    @click="handleUpdateField('position', settingsData.position)"
                    class="btn-secondary whitespace-nowrap"
                    :disabled="settingsData.position === user?.position"
                  >
                    Изменить
                  </button>
                </div>
              </div>

              <!-- Имя и Фамилия -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Имя</label>
                  <div class="flex gap-2">
                    <input
                      v-model="settingsData.first_name"
                      type="text"
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 flex-1"
                      :placeholder="user?.first_name"
                    />
                    <button
                      @click="handleUpdateField('first_name', settingsData.first_name)"
                      class="btn-secondary whitespace-nowrap"
                      :disabled="!settingsData.first_name || settingsData.first_name === user?.first_name"
                    >
                      ✓
                    </button>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Фамилия</label>
                  <div class="flex gap-2">
                    <input
                      v-model="settingsData.last_name"
                      type="text"
                      class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 flex-1"
                      :placeholder="user?.last_name"
                    />
                    <button
                      @click="handleUpdateField('last_name', settingsData.last_name)"
                      class="btn-secondary whitespace-nowrap"
                      :disabled="!settingsData.last_name || settingsData.last_name === user?.last_name"
                    >
                      ✓
                    </button>
                  </div>
                </div>
              </div>
                </div>
              </div>

              <!-- Аккордеон: Уведомления -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button
                  @click="toggleSection('notifications')"
                  class="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <BellIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <span class="font-medium text-gray-900 dark:text-gray-100">Уведомления</span>
                  </div>
                  <ChevronDownIcon
                    :class="[
                      'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
                      expandedSections.notifications ? 'rotate-180' : ''
                    ]"
                  />
                </button>
                <div v-show="expandedSections.notifications" class="p-4 bg-white dark:bg-gray-800">
                  <div class="space-y-4">
              <!-- Push уведомления -->
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Push-уведомления</label>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Получать уведомления о новых сообщениях и событиях
                  </p>
                </div>
                <button
                  @click="togglePushNotifications"
                  :class="[
                    'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                    notificationSettings.pushEnabled ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-600'
                  ]"
                >
                  <span
                    :class="[
                      'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                      notificationSettings.pushEnabled ? 'translate-x-6' : 'translate-x-1'
                    ]"
                  ></span>
                </button>
              </div>

              <!-- Звуковые уведомления -->
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Звуковые уведомления</label>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Воспроизводить звук при получении сообщений
                  </p>
                </div>
                <button
                  @click="toggleSoundNotifications"
                  :class="[
                    'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                    notificationSettings.soundEnabled ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-600'
                  ]"
                >
                  <span
                    :class="[
                      'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                      notificationSettings.soundEnabled ? 'translate-x-6' : 'translate-x-1'
                    ]"
                  ></span>
                </button>
              </div>

              <!-- Уведомления на email -->
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email уведомления</label>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Получать важные уведомления на почту
                  </p>
                </div>
                <button
                  @click="toggleEmailNotifications"
                  :class="[
                    'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                    notificationSettings.emailEnabled ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-600'
                  ]"
                >
                  <span
                    :class="[
                      'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                      notificationSettings.emailEnabled ? 'translate-x-6' : 'translate-x-1'
                    ]"
                  ></span>
                </button>
              </div>
                  </div>
                </div>
              </div>

              <!-- Аккордеон: Разрешения -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button
                  @click="toggleSection('permissions')"
                  class="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <ShieldCheckIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <span class="font-medium text-gray-900 dark:text-gray-100">Разрешения</span>
                  </div>
                  <ChevronDownIcon
                    :class="[
                      'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
                      expandedSections.permissions ? 'rotate-180' : ''
                    ]"
                  />
                </button>
                <div v-show="expandedSections.permissions" class="p-4 bg-white dark:bg-gray-800">
                  <div class="space-y-4">
              <!-- Камера -->
              <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="flex items-center gap-3 flex-1">
                  <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                    <CameraIcon class="w-6 h-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Камера</label>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ permissions.camera ? 'Разрешено' : 'Не разрешено' }}
                    </p>
                  </div>
                </div>
                <button
                  @click="requestCameraPermission"
                  class="btn-secondary text-sm"
                >
                  {{ permissions.camera ? 'Отозвать' : 'Разрешить' }}
                </button>
              </div>

              <!-- Фотоальбом -->
              <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="flex items-center gap-3 flex-1">
                  <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
                    <PhotoIcon class="w-6 h-6 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Фотоальбом</label>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ permissions.photos ? 'Разрешено' : 'Не разрешено' }}
                    </p>
                  </div>
                </div>
                <button
                  @click="requestPhotosPermission"
                  class="btn-secondary text-sm"
                >
                  {{ permissions.photos ? 'Отозвать' : 'Разрешить' }}
                </button>
              </div>

              <!-- Хранилище -->
              <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="flex items-center gap-3 flex-1">
                  <div class="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                    <CircleStackIcon class="w-6 h-6 text-green-600 dark:text-green-400" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Хранилище</label>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ permissions.storage ? 'Разрешено' : 'Не разрешено' }}
                    </p>
                  </div>
                </div>
                <button
                  @click="requestStoragePermission"
                  class="btn-secondary text-sm"
                >
                  {{ permissions.storage ? 'Отозвать' : 'Разрешить' }}
                </button>
              </div>

              <!-- Микрофон -->
              <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="flex items-center gap-3 flex-1">
                  <div class="w-10 h-10 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center">
                    <MicrophoneIcon class="w-6 h-6 text-red-600 dark:text-red-400" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Микрофон</label>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ permissions.microphone ? 'Разрешено' : 'Не разрешено' }}
                    </p>
                  </div>
                </div>
                <button
                  @click="requestMicrophonePermission"
                  class="btn-secondary text-sm"
                >
                  {{ permissions.microphone ? 'Отозвать' : 'Разрешить' }}
                </button>
              </div>
                  </div>
                </div>
              </div>

              <!-- Аккордеон: Внешний вид -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button
                  @click="toggleSection('appearance')"
                  class="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <PaintBrushIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <span class="font-medium text-gray-900 dark:text-gray-100">Внешний вид</span>
                  </div>
                  <ChevronDownIcon
                    :class="[
                      'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
                      expandedSections.appearance ? 'rotate-180' : ''
                    ]"
                  />
                </button>
                <div v-show="expandedSections.appearance" class="p-4 bg-white dark:bg-gray-800">
                  <div class="space-y-6">
                    <!-- Тема -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Тема оформления</label>
                      <div class="flex gap-3">
                        <button
                          @click="themeStore.setTheme(false)"
                          :class="[
                            'flex-1 p-4 rounded-lg border-2 transition-all',
                            !themeStore.isDark
                              ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                              : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                          ]"
                        >
                          <SunIcon class="w-8 h-8 mx-auto mb-2 text-yellow-500" />
                          <p class="text-sm font-medium text-gray-900 dark:text-gray-100">Светлая</p>
                        </button>
                        <button
                          @click="themeStore.setTheme(true)"
                          :class="[
                            'flex-1 p-4 rounded-lg border-2 transition-all',
                            themeStore.isDark
                              ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                              : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                          ]"
                        >
                          <MoonIcon class="w-8 h-8 mx-auto mb-2 text-blue-500" />
                          <p class="text-sm font-medium text-gray-900 dark:text-gray-100">Темная</p>
                        </button>
                      </div>
                    </div>

                    <!-- Основной цвет -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Основной цвет</label>
                      <div class="grid grid-cols-3 gap-3">
                        <button
                          v-for="preset in colorPresets"
                          :key="preset.value"
                          @click="updatePrimaryColor(preset.value)"
                          :class="[
                            'p-3 rounded-lg border-2 transition-all',
                            themeSettings.primaryColor === preset.value
                              ? 'border-gray-900 dark:border-white scale-105'
                              : 'border-gray-300 dark:border-gray-600 hover:scale-105'
                          ]"
                        >
                          <div
                            class="w-full h-8 rounded mb-2"
                            :style="{ backgroundColor: preset.value }"
                          ></div>
                          <p class="text-xs font-medium text-gray-900 dark:text-gray-100">{{ preset.name }}</p>
                        </button>
                      </div>
                      <div class="mt-3 flex items-center gap-3">
                        <input
                          type="color"
                          :value="themeSettings.primaryColor"
                          @input="updatePrimaryColor($event.target.value)"
                          class="w-12 h-12 rounded cursor-pointer"
                        />
                        <span class="text-sm text-gray-600 dark:text-gray-400">Или выберите свой цвет</span>
                      </div>
                    </div>

                    <!-- Размер шрифта -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Размер шрифта</label>
                      <div class="flex gap-3">
                        <button
                          v-for="size in fontSizes"
                          :key="size.value"
                          @click="updateFontSize(size.value)"
                          :class="[
                            'flex-1 p-3 rounded-lg border-2 transition-all',
                            themeSettings.fontSize === size.value
                              ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                              : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                          ]"
                        >
                          <p class="font-medium text-gray-900 dark:text-gray-100">{{ size.name }}</p>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Аккордеон: Звуковые уведомления -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button
                  @click="toggleSection('sounds')"
                  class="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <SpeakerWaveIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <span class="font-medium text-gray-900 dark:text-gray-100">Звуковые уведомления</span>
                  </div>
                  <ChevronDownIcon
                    :class="[
                      'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
                      expandedSections.sounds ? 'rotate-180' : ''
                    ]"
                  />
                </button>
                <div v-show="expandedSections.sounds" class="p-4 bg-white dark:bg-gray-800">
                  <div class="space-y-6">
                    <!-- Включение звуков -->
                    <div class="flex items-center justify-between">
                      <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Звуки сообщений</label>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Воспроизводить звук при получении новых сообщений</p>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          v-model="soundSettings.enabled"
                          @change="saveSoundSettings"
                          class="sr-only peer"
                        />
                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
                      </label>
                    </div>

                    <!-- Выбор звука -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Звук уведомления</label>
                      <div class="flex gap-2">
                        <select
                          v-model="soundSettings.selectedSound"
                          @change="saveSoundSettings"
                          class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                        >
                          <option v-for="sound in availableSounds" :key="sound.id" :value="sound.id">
                            {{ sound.name }}
                          </option>
                        </select>
                        <button
                          @click="refreshSoundsList"
                          class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                          title="Обновить список звуков"
                        >
                          <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                          </svg>
                        </button>
                      </div>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        Добавьте MP3 файлы в папку sounds и нажмите кнопку обновления
                      </p>
                    </div>

                    <!-- Громкость -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                        Громкость: {{ Math.round(soundSettings.volume * 100) }}%
                      </label>
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        v-model.number="soundSettings.volume"
                        @change="saveSoundSettings"
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
                      />
                    </div>

                    <!-- Тест звука -->
                    <button
                      @click="testSound"
                      class="w-full btn-secondary flex items-center justify-center gap-2"
                    >
                      <SpeakerWaveIcon class="w-5 h-5" />
                      Проверить звук
                    </button>

                    <!-- Загрузка своего звука -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Загрузить свой звук</label>
                      <input
                        type="file"
                        accept="audio/*"
                        @change="uploadCustomSound"
                        class="block w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 dark:file:bg-primary-900/20 dark:file:text-primary-400"
                      />
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Поддерживаются форматы: MP3, WAV, OGG</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Аккордеон: Безопасность -->
              <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button
                  @click="toggleSection('security')"
                  class="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <LockClosedIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <span class="font-medium text-gray-900 dark:text-gray-100">Безопасность</span>
                  </div>
                  <ChevronDownIcon
                    :class="[
                      'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
                      expandedSections.security ? 'rotate-180' : ''
                    ]"
                  />
                </button>
                <div v-show="expandedSections.security" class="p-4 bg-white dark:bg-gray-800">
                  <div class="space-y-4">
                    <h4 class="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">Изменить пароль</h4>
                    <form @submit.prevent="handleChangePassword" class="space-y-4">
                      <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Текущий пароль</label>
                        <input
                          v-model="passwordData.current_password"
                          type="password"
                          class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 w-full"
                        />
                      </div>
                      
                      <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Новый пароль</label>
                        <input
                          v-model="passwordData.new_password"
                          type="password"
                          class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 w-full"
                        />
                      </div>
                      
                      <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Подтвердите пароль</label>
                        <input
                          v-model="passwordData.confirm_password"
                          type="password"
                          class="input bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 w-full"
                        />
                      </div>
                      
                      <button type="submit" class="btn-primary w-full">
                        Изменить пароль
                      </button>
                    </form>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useNotificationSounds } from '@/composables/useNotificationSounds'
import api from '@/services/api'
import {
  CameraIcon,
  PhotoIcon,
  CircleStackIcon,
  MicrophoneIcon,
  ChevronDownIcon,
  UserCircleIcon,
  BellIcon,
  ShieldCheckIcon,
  LockClosedIcon,
  PaintBrushIcon,
  MoonIcon,
  SunIcon,
  SpeakerWaveIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const { soundSettings, availableSounds, playSound, saveSettings: saveSoundSettings, scanSoundsFolder } = useNotificationSounds()

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  if (!user.value) return '?'
  return `${user.value.first_name?.[0] || ''}${user.value.last_name?.[0] || ''}`
})

const settingsData = ref({
  username: '',
  email: '',
  phone: '',
  position: '',
  first_name: '',
  last_name: '',
  status: 'online'
})

const passwordData = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const settingsPhoneError = ref('')
const avatarInput = ref(null)

// Настройки уведомлений
const notificationSettings = ref({
  pushEnabled: false,
  soundEnabled: true,
  emailEnabled: false
})

// Разрешения
const permissions = ref({
  camera: false,
  photos: false,
  storage: false,
  microphone: false
})

// Состояние аккордеона
const expandedSections = ref({
  basic: false,
  notifications: false,
  permissions: false,
  sounds: false,
  security: false,
  appearance: false
})

// Настройки внешнего вида
const themeSettings = ref({
  primaryColor: localStorage.getItem('primaryColor') || '#3b82f6',
  accentColor: localStorage.getItem('accentColor') || '#10b981',
  fontSize: localStorage.getItem('fontSize') || 'medium'
})

const colorPresets = [
  { name: 'Синий', value: '#3b82f6' },
  { name: 'Зеленый', value: '#10b981' },
  { name: 'Фиолетовый', value: '#8b5cf6' },
  { name: 'Розовый', value: '#ec4899' },
  { name: 'Оранжевый', value: '#f59e0b' },
  { name: 'Красный', value: '#ef4444' }
]

const fontSizes = [
  { name: 'Маленький', value: 'small' },
  { name: 'Средний', value: 'medium' },
  { name: 'Большой', value: 'large' }
]

// Переключение секций аккордеона
function toggleSection(section) {
  expandedSections.value[section] = !expandedSections.value[section]
}

onMounted(() => {
  loadNotificationSettings()
  checkPermissions()
  applyThemeSettings()
  if (user.value) {
    settingsData.value = {
      username: '',
      email: '',
      phone: '',
      position: '',
      first_name: '',
      last_name: '',
      status: user.value.status || 'online'
    }
  }
})

function getPhoneDisplay(phone) {
  if (!phone) return ''
  if (phone.startsWith('+7')) {
    return phone.substring(2)
  }
  return phone
}

function validateSettingsPhone() {
  const phone = settingsData.value.phone
  
  // Удаляем все нецифровые символы
  settingsData.value.phone = phone.replace(/\D/g, '')
  
  if (settingsData.value.phone && settingsData.value.phone.length !== 9) {
    settingsPhoneError.value = 'Номер должен содержать 9 цифр'
  } else if (settingsData.value.phone && !settingsData.value.phone.startsWith('9')) {
    settingsPhoneError.value = 'Номер должен начинаться с 9'
  } else {
    settingsPhoneError.value = ''
  }
}

async function handleUpdateField(field, value) {
  if (settingsPhoneError.value && field === 'phone') {
    alert('Исправьте ошибки в номере телефона')
    return
  }

  try {
    const updateData = { [field]: value }
    await api.put('/users/me', updateData)
    await authStore.checkAuth()
    
    // Очищаем поле после успешного обновления
    if (field !== 'status') {
      settingsData.value[field] = ''
    }
    
    alert('Настройка обновлена')
  } catch (error) {
    console.error('Update field error:', error)
    alert('Ошибка обновления: ' + (error.response?.data?.detail || error.message))
  }
}

async function handleChangePassword() {
  if (passwordData.value.new_password !== passwordData.value.confirm_password) {
    alert('Пароли не совпадают')
    return
  }
  
  try {
    await api.post('/users/change-password', {
      current_password: passwordData.value.current_password,
      new_password: passwordData.value.new_password
    })
    
    passwordData.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
    
    alert('Пароль изменен')
  } catch (error) {
    console.error('Change password error:', error)
    alert('Ошибка изменения пароля')
  }
}

async function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const uploadResponse = await api.post('/messages/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    // Обновляем аватар пользователя
    await api.put('/users/me', {
      avatar_url: uploadResponse.data.file_path
    })
    
    await authStore.checkAuth()
    alert('Фото обновлено')
  } catch (error) {
    console.error('Avatar upload error:', error)
    console.error('Error details:', error.response?.data)
    alert('Ошибка загрузки фото: ' + (error.response?.data?.detail || error.message))
  }
}

// Загрузка настроек уведомлений
function loadNotificationSettings() {
  const saved = localStorage.getItem('notificationSettings')
  if (saved) {
    notificationSettings.value = JSON.parse(saved)
  }
}

// Сохранение настроек уведомлений
function saveNotificationSettings() {
  localStorage.setItem('notificationSettings', JSON.stringify(notificationSettings.value))
}

// Переключение push-уведомлений
async function togglePushNotifications() {
  if (!notificationSettings.value.pushEnabled) {
    // Запрос разрешения на уведомления
    if ('Notification' in window) {
      const permission = await Notification.requestPermission()
      if (permission === 'granted') {
        notificationSettings.value.pushEnabled = true
        saveNotificationSettings()
        alert('Push-уведомления включены')
      } else {
        alert('Разрешение на уведомления отклонено')
      }
    } else {
      alert('Ваш браузер не поддерживает уведомления')
    }
  } else {
    notificationSettings.value.pushEnabled = false
    saveNotificationSettings()
    alert('Push-уведомления отключены')
  }
}

// Переключение звуковых уведомлений
function toggleSoundNotifications() {
  notificationSettings.value.soundEnabled = !notificationSettings.value.soundEnabled
  saveNotificationSettings()
}

// Переключение email уведомлений
function toggleEmailNotifications() {
  notificationSettings.value.emailEnabled = !notificationSettings.value.emailEnabled
  saveNotificationSettings()
}

// Проверка разрешений
async function checkPermissions() {
  // Проверка разрешения на уведомления
  if ('Notification' in window) {
    permissions.value.notifications = Notification.permission === 'granted'
  }

  // Проверка других разрешений через Permissions API
  if ('permissions' in navigator) {
    try {
      const cameraPermission = await navigator.permissions.query({ name: 'camera' })
      permissions.value.camera = cameraPermission.state === 'granted'
      
      const microphonePermission = await navigator.permissions.query({ name: 'microphone' })
      permissions.value.microphone = microphonePermission.state === 'granted'
    } catch (error) {
      console.log('Permissions API not fully supported')
    }
  }

  // Проверка localStorage для хранилища
  try {
    localStorage.setItem('test', 'test')
    localStorage.removeItem('test')
    permissions.value.storage = true
  } catch (error) {
    permissions.value.storage = false
  }
}

// Запрос разрешения на камеру
async function requestCameraPermission() {
  if (permissions.value.camera) {
    alert('Чтобы отозвать разрешение, перейдите в настройки браузера')
    return
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    stream.getTracks().forEach(track => track.stop())
    permissions.value.camera = true
    alert('Разрешение на камеру получено')
  } catch (error) {
    alert('Не удалось получить доступ к камере')
  }
}

// Запрос разрешения на фотоальбом
async function requestPhotosPermission() {
  if (permissions.value.photos) {
    permissions.value.photos = false
    alert('Разрешение отозвано')
    return
  }

  // Создаем input для выбора файла
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = () => {
    permissions.value.photos = true
    alert('Разрешение на фотоальбом получено')
  }
  input.click()
}

// Запрос разрешения на хранилище
function requestStoragePermission() {
  if (permissions.value.storage) {
    alert('Хранилище уже доступно')
    return
  }

  try {
    localStorage.setItem('permission_test', 'test')
    localStorage.removeItem('permission_test')
    permissions.value.storage = true
    alert('Разрешение на хранилище получено')
  } catch (error) {
    alert('Не удалось получить доступ к хранилищу')
  }
}

// Запрос разрешения на микрофон
async function requestMicrophonePermission() {
  if (permissions.value.microphone) {
    alert('Чтобы отозвать разрешение, перейдите в настройки браузера')
    return
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    stream.getTracks().forEach(track => track.stop())
    permissions.value.microphone = true
    alert('Разрешение на микрофон получено')
  } catch (error) {
    alert('Не удалось получить доступ к микрофону')
  }
}

// Настройки внешнего вида
function applyThemeSettings() {
  console.log('Applying theme settings:', themeSettings.value)
  
  // Применяем основной цвет
  document.documentElement.style.setProperty('--primary-color', themeSettings.value.primaryColor)
  document.documentElement.style.setProperty('--accent-color', themeSettings.value.accentColor)
  
  // Применяем размер шрифта
  const fontSizeMap = {
    small: '14px',
    medium: '16px',
    large: '18px'
  }
  const fontSize = fontSizeMap[themeSettings.value.fontSize] || '16px'
  document.documentElement.style.fontSize = fontSize
  
  console.log('Theme applied:', {
    primaryColor: themeSettings.value.primaryColor,
    fontSize: fontSize
  })
}

function updatePrimaryColor(color) {
  console.log('Updating primary color to:', color)
  themeSettings.value.primaryColor = color
  localStorage.setItem('primaryColor', color)
  applyThemeSettings()
}

function updateAccentColor(color) {
  themeSettings.value.accentColor = color
  localStorage.setItem('accentColor', color)
  applyThemeSettings()
}

function updateFontSize(size) {
  console.log('Updating font size to:', size)
  themeSettings.value.fontSize = size
  localStorage.setItem('fontSize', size)
  applyThemeSettings()
}

// Функции для звуковых уведомлений
function testSound() {
  playSound()
}

async function refreshSoundsList() {
  await scanSoundsFolder()
  alert('Список звуков обновлен! Найдено звуков: ' + availableSounds.value.length)
}

async function uploadCustomSound(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // Проверка типа файла
  if (!file.type.startsWith('audio/')) {
    alert('Пожалуйста, выберите аудио файл')
    return
  }
  
  // Проверка размера (макс 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('Файл слишком большой. Максимальный размер: 5MB')
    return
  }
  
  try {
    // Читаем файл как Data URL
    const reader = new FileReader()
    reader.onload = (e) => {
      // Сохраняем в localStorage
      localStorage.setItem('customSound', e.target.result)
      soundSettings.value.selectedSound = 'custom'
      saveSoundSettings()
      alert('Звук успешно загружен!')
    }
    reader.readAsDataURL(file)
  } catch (error) {
    console.error('Upload sound error:', error)
    alert('Ошибка загрузки звука')
  }
}
</script>
