<template>
  <div class="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <button @click="$router.go(-1)" class="mr-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            <ArrowLeftIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
          
          <button @click="goToUserProfile" class="flex items-center hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg p-2 -ml-2 transition-colors">
            <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
              {{ chat?.name?.[0] || '?' }}
            </div>
            
            <div class="ml-3 text-left min-w-[150px]">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 h-7 flex items-center">
                {{ chat?.name || 'Загрузка...' }}
              </h2>
              <div class="h-5 flex items-center">
                <p v-if="typingUsers.size > 0" class="text-sm text-primary-600 dark:text-primary-400">
                  <span class="animate-pulse">печатает...</span>
                </p>
                <p v-else-if="isConnected" class="text-xs text-green-600 dark:text-green-400">онлайн</p>
                <p v-else class="text-xs text-gray-400 dark:text-gray-500">офлайн</p>
              </div>
            </div>
          </button>
        </div>
        
        <div class="flex items-center space-x-2">
          <button @click="showSearch = !showSearch" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors" title="Поиск">
            <MagnifyingGlassIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
          
          <Menu as="div" class="relative">
            <MenuButton class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <EllipsisVerticalIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </MenuButton>
          
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute right-0 mt-2 w-48 origin-top-right bg-white dark:bg-gray-800 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
              <div class="p-1">
                <MenuItem v-if="chat?.chat_type === 'group'" v-slot="{ active }">
                  <button
                    @click="showGroupSettings = true"
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      'group flex items-center w-full px-3 py-2 text-sm text-gray-900 dark:text-gray-100 rounded-md'
                    ]"
                  >
                    <Cog6ToothIcon class="w-5 h-5 mr-2" />
                    Настройки группы
                  </button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="toggleChatSound"
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      'group flex items-center w-full px-3 py-2 text-sm text-gray-900 dark:text-gray-100 rounded-md'
                    ]"
                  >
                    <SpeakerWaveIcon v-if="!isChatMuted" class="w-5 h-5 mr-2" />
                    <SpeakerXMarkIcon v-else class="w-5 h-5 mr-2" />
                    {{ isChatMuted ? 'Включить звук' : 'Отключить звук' }}
                  </button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="renameChatPrompt"
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      'group flex items-center w-full px-3 py-2 text-sm text-gray-900 dark:text-gray-100 rounded-md'
                    ]"
                  >
                    <PencilIcon class="w-5 h-5 mr-2" />
                    Переименовать
                  </button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="clearChatHistory"
                    :class="[
                      active ? 'bg-orange-50 dark:bg-orange-900 text-orange-600 dark:text-orange-400' : 'text-gray-900 dark:text-gray-100',
                      'group flex items-center w-full px-3 py-2 text-sm rounded-md'
                    ]"
                  >
                    <TrashIcon class="w-5 h-5 mr-2" />
                    Очистить историю
                  </button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="deleteChat"
                    :class="[
                      active ? 'bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-400' : 'text-red-600 dark:text-red-400',
                      'group flex items-center w-full px-3 py-2 text-sm rounded-md font-semibold'
                    ]"
                  >
                    <TrashIcon class="w-5 h-5 mr-2" />
                    Удалить чат
                  </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
        </div>
      </div>
    </div>
    
    <!-- Search Panel -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform -translate-y-full opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-full opacity-0"
    >
      <div v-if="showSearch" class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-center space-x-2">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Поиск в сообщениях..."
            class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            autofocus
          />
          <button @click="showSearch = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            <XMarkIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
        </div>
        
        <!-- Search Results -->
        <div v-if="searchResults.length > 0" class="mt-4 max-h-60 overflow-y-auto space-y-2">
          <div
            v-for="result in searchResults"
            :key="result.id"
            @click="scrollToMessage(result.id)"
            class="p-3 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
          >
            <p class="text-sm text-gray-900 dark:text-gray-100">{{ result.content }}</p>
            <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatTime(result.created_at) }}</span>
          </div>
        </div>
        <div v-else-if="searchQuery" class="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
          Ничего не найдено
        </div>
      </div>
    </transition>
    
    <!-- Pinned Messages Panel -->
    <div v-if="pinnedMessages.length > 0" class="bg-primary-50 dark:bg-primary-900/20 border-b border-primary-200 dark:border-primary-800 p-3">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2 flex-1 min-w-0">
          <BookmarkIcon class="w-5 h-5 text-primary-600 dark:text-primary-400 flex-shrink-0" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-primary-900 dark:text-primary-100">Закрепленное сообщение</p>
            <p class="text-sm text-primary-700 dark:text-primary-300 truncate">{{ pinnedMessages[0].content }}</p>
          </div>
        </div>
        <button @click="scrollToMessage(pinnedMessages[0].id)" class="p-1 hover:bg-primary-100 dark:hover:bg-primary-800 rounded flex-shrink-0">
          <ChevronDownIcon class="w-5 h-5 text-primary-600 dark:text-primary-400" />
        </button>
      </div>
    </div>
    
    <!-- Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
      <div v-if="messages.length === 0" class="text-center py-12">
        <ChatBubbleLeftRightIcon class="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p class="text-gray-500 dark:text-gray-400">Нет сообщений. Начните общение!</p>
      </div>
      
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'flex transition-all duration-300',
          message.sender_id === currentUserId ? 'justify-end' : 'justify-start',
          message.isNew ? 'animate-slide-in' : ''
        ]"
      >
        <div class="relative group">
        <!-- Pinned Indicator -->
        <div v-if="message.is_pinned" class="absolute -top-2 -right-2 z-10">
          <div class="bg-primary-600 rounded-full p-1 shadow-lg">
            <BookmarkIcon class="w-3 h-3 text-white" />
          </div>
        </div>
        
        <!-- Message Actions Menu -->
        <div
          v-if="message.sender_id === currentUserId"
          class="absolute -left-10 top-2 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col gap-1"
        >
          <button
            @click="togglePinMessage(message)"
            class="p-1.5 bg-white dark:bg-gray-700 rounded-full shadow-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            :title="message.is_pinned ? 'Открепить' : 'Закрепить'"
          >
            <BookmarkIcon :class="['w-4 h-4', message.is_pinned ? 'text-primary-600' : 'text-gray-600 dark:text-gray-300']" />
          </button>
          <button
            v-if="!message.content?.startsWith('📩 Переслано:')"
            @click="startEditMessage(message)"
            class="p-1.5 bg-white dark:bg-gray-700 rounded-full shadow-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            title="Редактировать"
          >
            <PencilIcon class="w-4 h-4 text-gray-600 dark:text-gray-300" />
          </button>
          <button
            @click="startForwardMessage(message)"
            class="p-1.5 bg-white dark:bg-gray-700 rounded-full shadow-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            title="Переслать"
          >
            <ArrowUturnRightIcon class="w-4 h-4 text-gray-600 dark:text-gray-300" />
          </button>
          <button
            @click="deleteMessage(message.id)"
            class="p-1.5 bg-white dark:bg-gray-700 rounded-full shadow-lg hover:bg-red-50 dark:hover:bg-red-900 transition-colors"
            title="Удалить"
          >
            <TrashIcon class="w-4 h-4 text-red-600 dark:text-red-400" />
          </button>
        </div>
        
        <div
          :id="`message-${message.id}`"
          @click="showReactionPicker(message.id)"
          :class="[
            'max-w-md px-4 py-2 rounded-2xl cursor-pointer transition-all duration-200',
            message.sender_id === currentUserId
              ? 'bg-primary-600 text-white rounded-br-sm hover:bg-primary-700'
              : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-bl-sm shadow-sm hover:shadow-md',
            message.isEdited ? 'border-2 border-yellow-400' : ''
          ]"
        >
          <!-- Reply -->
          <div
            v-if="message.reply_to"
            :class="[
              'mb-2 p-2 rounded-lg border-l-2',
              message.sender_id === currentUserId
                ? 'bg-primary-700 border-primary-400'
                : 'bg-gray-100 border-gray-400'
            ]"
          >
            <p class="text-xs opacity-75 truncate">
              Ответ на: {{ message.reply_to.content }}
            </p>
          </div>
          
          <!-- Content -->
          <p v-if="message.content" class="text-sm break-words">
            {{ message.content }}
            <span v-if="message.isEdited" class="text-xs opacity-60 ml-2">(изменено)</span>
          </p>
          
          <!-- Attachments -->
          <div v-if="message.attachments?.length" class="mt-2 space-y-2">
            <div v-for="attachment in message.attachments" :key="attachment.id">
              <img
                v-if="attachment.file_type.startsWith('image/')"
                :src="`http://localhost:8000${attachment.file_path}`"
                :alt="attachment.file_name"
                class="max-w-xs rounded-lg"
              />
              
              <audio
                v-else-if="attachment.file_type.startsWith('audio/')"
                :src="`http://localhost:8000${attachment.file_path}`"
                controls
                class="w-full max-w-xs"
              />
              
              <button
                v-else
                @click="openDocument(attachment)"
                :class="[
                  'flex items-center p-2 rounded-lg w-full text-left',
                  message.sender_id === currentUserId
                    ? 'bg-primary-700 hover:bg-primary-800'
                    : 'bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600'
                ]"
              >
                <DocumentIcon class="w-5 h-5 mr-2" />
                <span class="text-sm">{{ attachment.file_name }}</span>
              </button>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="flex items-center justify-between mt-1">
            <span class="text-xs opacity-75">
              {{ formatTime(message.created_at) }}
            </span>
          </div>
          
          <!-- Reactions -->
          <div v-if="message.reactions?.length" class="flex flex-wrap gap-1 mt-2">
            <button
              v-for="(reaction, index) in message.reactions"
              :key="index"
              class="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-xs hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              {{ reaction.emoji }} {{ reaction.count }}
            </button>
          </div>
        </div>
        
        <!-- Reaction Picker -->
        <div
          v-if="selectedMessageForReaction === message.id"
          @click.stop
          class="absolute bottom-full mb-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-2 flex gap-1 z-10"
        >
          <button
            v-for="emoji in quickReactions"
            :key="emoji"
            @click="addReaction(message.id, emoji)"
            class="text-2xl hover:scale-125 transition-transform p-1"
          >
            {{ emoji }}
          </button>
        </div>
        </div>
      </div>
    </div>
    
    <!-- Drag & Drop Overlay -->
    <div
      v-if="isDragging"
      class="fixed inset-0 bg-primary-600 bg-opacity-90 z-50 flex items-center justify-center"
      @drop.prevent="handleDrop"
      @dragover.prevent
      @dragleave="isDragging = false"
    >
      <div class="text-center text-white">
        <DocumentIcon class="w-24 h-24 mx-auto mb-4" />
        <h2 class="text-3xl font-bold mb-2">Отпустите файлы здесь</h2>
        <p class="text-xl">Файлы будут загружены в чат</p>
      </div>
    </div>

    <!-- File Preview Modal -->
    <TransitionRoot :show="showFilePreview" as="template">
      <Dialog @close="showFilePreview = false" class="relative z-50">
        <TransitionChild
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-75" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4">
            <TransitionChild
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 shadow-xl transition-all">
                <DialogTitle class="text-lg font-semibold text-gray-900 mb-4">
                  Предпросмотр файлов ({{ previewFiles.length }})
                </DialogTitle>
                
                <div class="space-y-4 max-h-96 overflow-y-auto">
                  <div
                    v-for="(file, index) in previewFiles"
                    :key="index"
                    class="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg"
                  >
                    <img
                      v-if="file.type.startsWith('image/')"
                      :src="file.preview"
                      class="w-16 h-16 object-cover rounded"
                    />
                    <DocumentIcon v-else class="w-16 h-16 text-gray-400" />
                    
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
                      <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
                    </div>
                    
                    <button
                      @click="removePreviewFile(index)"
                      class="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                    >
                      <XMarkIcon class="w-5 h-5" />
                    </button>
                  </div>
                </div>
                
                <div class="mt-6 flex space-x-3">
                  <button
                    @click="uploadPreviewFiles"
                    :disabled="uploading"
                    class="flex-1 btn-primary disabled:opacity-50"
                  >
                    {{ uploading ? 'Загрузка...' : 'Отправить' }}
                  </button>
                  <button
                    @click="showFilePreview = false"
                    class="flex-1 btn-secondary"
                  >
                    Отмена
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Edit Message Bar -->
    <div
      v-if="editingMessage"
      class="bg-yellow-50 dark:bg-yellow-900/20 border-t border-yellow-200 dark:border-yellow-800 p-3 flex items-center justify-between"
    >
      <div class="flex items-center gap-2">
        <PencilIcon class="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
        <div>
          <p class="text-sm font-medium text-yellow-900 dark:text-yellow-100">Редактирование сообщения</p>
          <p class="text-xs text-yellow-700 dark:text-yellow-300 truncate max-w-xs">{{ editingMessage.content }}</p>
        </div>
      </div>
      <button
        @click="cancelEdit"
        class="p-1 hover:bg-yellow-100 dark:hover:bg-yellow-800 rounded transition-colors"
      >
        <XMarkIcon class="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
      </button>
    </div>

    <!-- Forward Message Modal -->
    <TransitionRoot :show="showForwardModal" as="template">
      <Dialog @close="showForwardModal = false" class="relative z-50">
        <TransitionChild
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-75" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4">
            <TransitionChild
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-xl transition-all">
                <DialogTitle class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                  Переслать сообщение
                </DialogTitle>
                
                <div class="space-y-2 max-h-96 overflow-y-auto mb-4">
                  <button
                    v-for="chat in availableChats"
                    :key="chat.id"
                    @click="forwardToChat(chat.id)"
                    class="w-full flex items-center p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors text-left"
                  >
                    <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-semibold">
                      {{ chat.name?.[0] || '?' }}
                    </div>
                    <div class="ml-3">
                      <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ chat.name }}</p>
                    </div>
                  </button>
                </div>
                
                <button
                  @click="showForwardModal = false"
                  class="w-full btn-secondary"
                >
                  Отмена
                </button>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Input -->
    <div class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 p-3">
      <!-- Upload Progress -->
      <div v-if="uploadProgress > 0 && uploadProgress < 100" class="mb-2">
        <div class="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-1">
          <span>Загрузка файла...</span>
          <span>{{ uploadProgress }}%</span>
        </div>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            class="bg-primary-600 h-2 rounded-full transition-all duration-300"
            :style="{ width: uploadProgress + '%' }"
          ></div>
        </div>
      </div>
      
      <div class="flex items-end space-x-2">
        <!-- Left buttons -->
        <Menu as="div" class="relative flex-shrink-0">
          <MenuButton
            class="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            title="Прикрепить файл"
          >
            <PlusIcon class="w-6 h-6" />
          </MenuButton>
          
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute bottom-full left-0 mb-2 w-48 origin-bottom-left bg-white dark:bg-gray-800 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <div class="p-1">
                <MenuItem v-slot="{ active }">
                  <button
                    @click="() => fileInput.click()"
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      'group flex items-center w-full px-3 py-2 text-sm text-gray-900 dark:text-gray-100 rounded-md'
                    ]"
                  >
                    <PhotoIcon class="w-5 h-5 mr-2" />
                    Изображение
                  </button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="() => documentInput.click()"
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      'group flex items-center w-full px-3 py-2 text-sm text-gray-900 dark:text-gray-100 rounded-md'
                    ]"
                  >
                    <DocumentIcon class="w-5 h-5 mr-2" />
                    Документ
                  </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
        
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          multiple
          class="hidden"
          @change="handleFileSelect"
        />
        <input
          ref="documentInput"
          type="file"
          accept=".pdf,.doc,.docx,.txt,.xlsx,.xls,.ppt,.pptx"
          multiple
          class="hidden"
          @change="handleFileSelect"
        />
        
        <button
          @click="showEmojiPicker = !showEmojiPicker"
          class="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors flex-shrink-0"
          title="Эмодзи"
        >
          <FaceSmileIcon class="w-6 h-6" />
        </button>
        
        <!-- Message input -->
        <div class="flex-1 bg-gray-100 dark:bg-gray-800 rounded-2xl px-4 py-2 min-h-[44px] max-h-32 overflow-y-auto">
          <textarea
            ref="messageInput"
            v-model="newMessage"
            placeholder="Введите сообщение..."
            class="w-full bg-transparent text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 resize-none focus:outline-none"
            rows="1"
            @input="handleTyping"
            @keydown.enter.exact.prevent="sendMessage"
            @keydown.enter.shift.exact="newMessage += '\n'"
          ></textarea>
        </div>
        
        <!-- Right buttons -->
        <button
          v-if="newMessage.trim()"
          @click="editingMessage ? updateMessage() : sendMessage()"
          :disabled="isSending"
          :class="[
            'p-3 rounded-full transition-all duration-200 flex-shrink-0',
            isSending
              ? 'bg-gray-400 cursor-not-allowed'
              : editingMessage
              ? 'bg-yellow-600 hover:bg-yellow-700'
              : 'bg-green-600 hover:bg-green-700 hover:scale-110',
            'text-white'
          ]"
          :title="editingMessage ? 'Сохранить' : 'Отправить'"
        >
          <PaperAirplaneIcon v-if="!isSending" class="w-5 h-5" :class="{ 'animate-pulse': isSending }" />
          <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        </button>
        
        <button
          v-else
          :class="[
            'p-3 rounded-full transition-colors flex-shrink-0',
            isRecording ? 'bg-red-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600 hover:text-gray-900 dark:hover:text-gray-200'
          ]"
          @mousedown="startRecording"
          @mouseup="stopRecording"
          @mouseleave="stopRecording"
          title="Голосовое сообщение"
        >
          <MicrophoneIcon class="w-5 h-5" />
        </button>
      </div>
    </div>
    
    <!-- Emoji Picker -->
    <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div v-if="showEmojiPicker" class="absolute bottom-20 right-6 rounded-lg shadow-xl">
        <emoji-picker
          @emoji-click="onEmojiSelect"
          :class="themeStore.isDark ? 'dark' : 'light'"
        ></emoji-picker>
      </div>
    </transition>
    
    <!-- Group Settings Modal -->
    <GroupSettingsModal
      :show="showGroupSettings"
      :chat-id="parseInt(route.params.id)"
      @close="showGroupSettings = false"
      @updated="loadChat"
      @left="handleLeftGroup"
    />
    
    <!-- Document Viewer -->
    <DocumentViewer
      :show="showDocumentViewer"
      :file-url="selectedDocument.url"
      :file-name="selectedDocument.name"
      @close="closeDocumentViewer"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useNotificationSounds } from '@/composables/useNotificationSounds'
import { useChatWebSocket } from '@/composables/useWebSocket'
import api from '@/services/api'
import {
  Menu,
  MenuButton,
  MenuItems,
  MenuItem,
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle
} from '@headlessui/vue'
import GroupSettingsModal from '@/components/GroupSettingsModal.vue'
import DocumentViewer from '@/components/DocumentViewer.vue'
import 'emoji-picker-element'
import {
  ArrowLeftIcon,
  EllipsisVerticalIcon,
  InformationCircleIcon,
  TrashIcon,
  PencilIcon,
  ChatBubbleLeftRightIcon,
  PhotoIcon,
  Cog6ToothIcon,
  PaperClipIcon,
  MicrophoneIcon,
  FaceSmileIcon,
  PaperAirplaneIcon,
  DocumentIcon,
  XMarkIcon,
  PlusIcon,
  ArrowUturnRightIcon,
  MagnifyingGlassIcon,
  BookmarkIcon,
  ChevronDownIcon,
  SpeakerWaveIcon,
  SpeakerXMarkIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const { playSound, soundSettings, saveSettings: saveSoundSettings } = useNotificationSounds()

// WebSocket
const { isConnected, typingUsers, sendTyping, markAsRead, websocket } = useChatWebSocket(computed(() => parseInt(route.params.id)))

const chat = ref(null)
const messages = ref([])
const newMessage = ref('')
const isTyping = ref(false)
const isRecording = ref(false)
const showEmojiPicker = ref(false)
const selectedMessageForReaction = ref(null)
const messagesContainer = ref(null)
const fileInput = ref(null)
const documentInput = ref(null)
const messageInput = ref(null)
const currentUserId = ref(authStore.user?.id)
const showGroupSettings = ref(false)

// Быстрые реакции (как в Telegram)
const quickReactions = ['👍', '❤️', '😂', '😮', '😢', '🙏', '👏']

// Автообновление сообщений
let messageUpdateInterval = null

// Drag & Drop
const isDragging = ref(false)
const showFilePreview = ref(false)
const previewFiles = ref([])
const uploading = ref(false)
const uploadProgress = ref(0)
const isSending = ref(false)
const editingMessage = ref(null)
const showForwardModal = ref(false)

// Search
const showSearch = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
let searchTimeout = null

// Pinned messages
const pinnedMessages = ref([])
const forwardingMessage = ref(null)
const availableChats = ref([])
const showDocumentViewer = ref(false)
const selectedDocument = ref({ url: '', name: '' })
const isDarkTheme = computed(() => document.documentElement.classList.contains('dark'))

onMounted(async () => {
  await loadChat()
  await loadMessages()
  await loadPinnedMessages()
  scrollToBottom()
  
  // Отмечаем сообщения как прочитанные
  await markMessagesAsRead()
  markAsRead() // Через WebSocket
  
  // Подписываемся на новые сообщения через WebSocket
  const unsubscribeNewMessage = websocket.on('new_message', async (data) => {
    if (data.chat_id === parseInt(route.params.id)) {
      // Добавляем новое сообщение с анимацией
      const newMsg = { ...data.message, isNew: true }
      messages.value.push(newMsg)
      
      // Воспроизводим звук если сообщение от другого пользователя
      if (data.message.sender_id !== authStore.user?.id) {
        playSound(data.chat_id)
      }
      
      // Убираем флаг анимации через 500ms
      setTimeout(() => {
        const msg = messages.value.find(m => m.id === newMsg.id)
        if (msg) msg.isNew = false
      }, 500)
      
      await nextTick()
      scrollToBottom()
      
      // Отмечаем как прочитанное ТОЛЬКО если страница видима и пользователь на этом чате
      if (!document.hidden && route.name === 'chat-detail') {
        markAsRead()
      }
    }
  })
  
  // Подписываемся на обновление сообщений
  const unsubscribeMessageUpdated = websocket.on('message_updated', (data) => {
    if (data.chat_id === parseInt(route.params.id)) {
      const msg = messages.value.find(m => m.id === data.message_id)
      if (msg) {
        msg.content = data.content
        msg.isEdited = true
      }
    }
  })
  
  // Подписываемся на удаление сообщений
  const unsubscribeMessageDeleted = websocket.on('message_deleted', (data) => {
    if (data.chat_id === parseInt(route.params.id)) {
      messages.value = messages.value.filter(m => m.id !== data.message_id)
    }
  })
  
  // Автообновление сообщений каждые 10 секунд (резервный механизм)
  messageUpdateInterval = setInterval(async () => {
    if (!isConnected.value) {
      // Если WebSocket отключен, загружаем сообщения через API
      const oldLength = messages.value.length
      await loadMessages()
      if (messages.value.length > oldLength) {
        scrollToBottom()
        await markMessagesAsRead()
      }
    }
  }, 10000)
  
  // Drag & Drop listeners
  window.addEventListener('dragenter', handleDragEnter)
  window.addEventListener('dragleave', handleDragLeave)
  window.addEventListener('dragover', (e) => e.preventDefault())
  window.addEventListener('drop', (e) => e.preventDefault())
  
  // Закрытие пикера реакций при клике вне
  document.addEventListener('click', closeReactionPicker)
  
  // Отмечаем сообщения как прочитанные при возвращении на страницу
  const handleVisibilityChange = () => {
    // Помечаем как прочитанные ТОЛЬКО если:
    // 1. Страница видима (не свернута)
    // 2. Мы находимся на странице чата
    // 3. ID чата совпадает с текущим
    if (!document.hidden && route.name === 'chat-detail' && route.params.id === String(parseInt(route.params.id))) {
      markAsRead()
      markMessagesAsRead()
    }
  }
  document.addEventListener('visibilitychange', handleVisibilityChange)
  
  // Очистка обработчика при размонтировании
  onBeforeUnmount(() => {
    document.removeEventListener('visibilitychange', handleVisibilityChange)
  })
})

// Отслеживаем переход на другую страницу
watch(() => route.name, (newName, oldName) => {
  // Если уходим со страницы чата на другую страницу
  if (oldName === 'chat-detail' && newName !== 'chat-detail') {
    // НЕ помечаем сообщения как прочитанные при уходе
    // Это предотвращает автоматическое обнуление счетчика
  }
  // Если приходим на страницу чата
  if (newName === 'chat-detail' && oldName !== 'chat-detail') {
    // Помечаем сообщения как прочитанные
    markAsRead()
    markMessagesAsRead()
  }
})

// Очистка при размонтировании
onBeforeUnmount(() => {
  if (messageUpdateInterval) {
    clearInterval(messageUpdateInterval)
  }
  document.removeEventListener('click', closeReactionPicker)
})

function handleDragEnter(e) {
  e.preventDefault()
  if (e.dataTransfer.types.includes('Files')) {
    isDragging.value = true
  }
}

function handleDragLeave(e) {
  e.preventDefault()
  if (e.target === document.body || e.target === document.documentElement) {
    isDragging.value = false
  }
}

function handleDrop(e) {
  e.preventDefault()
  isDragging.value = false
  
  const files = Array.from(e.dataTransfer.files)
  if (files.length > 0) {
    processFiles(files)
  }
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    processFiles(files)
  }
  // Reset input
  event.target.value = ''
}

async function processFiles(files) {
  const processedFiles = []
  
  for (const file of files) {
    const fileData = {
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      preview: null
    }
    
    // Create preview for images
    if (file.type.startsWith('image/')) {
      try {
        fileData.preview = await readFileAsDataURL(file)
      } catch (error) {
        console.error('Error reading file:', error)
      }
    }
    
    processedFiles.push(fileData)
  }
  
  previewFiles.value = processedFiles
  showFilePreview.value = true
}

function readFileAsDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

function removePreviewFile(index) {
  previewFiles.value.splice(index, 1)
  if (previewFiles.value.length === 0) {
    showFilePreview.value = false
  }
}

async function uploadPreviewFiles() {
  uploading.value = true
  
  try {
    for (const fileData of previewFiles.value) {
      await uploadSingleFile(fileData.file)
    }
    
    showFilePreview.value = false
    previewFiles.value = []
    await loadMessages()
    scrollToBottom()
  } catch (error) {
    console.error('Upload error:', error)
    alert('Ошибка загрузки файлов')
  } finally {
    uploading.value = false
  }
}

async function uploadSingleFile(file) {
  uploadProgress.value = 0
  
  const formData = new FormData()
  formData.append('file', file)
  
  const uploadResponse = await api.post('/messages/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
    }
  })
  
  const messageData = {
    chat_id: parseInt(route.params.id),
    content: file.name,
    message_type: file.type.startsWith('image/') ? 'image' : 'file',
    attachment: {
      file_name: uploadResponse.data.file_name,
      file_path: uploadResponse.data.file_path,
      file_type: uploadResponse.data.file_type,
      file_size: uploadResponse.data.file_size
    }
  }
  
  await api.post('/messages', messageData)
  uploadProgress.value = 0
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

async function loadChat() {
  try {
    const response = await api.get(`/chats/${route.params.id}`)
    chat.value = response.data
    
    // Для личных чатов обновляем название на ФИО собеседника
    if (chat.value.chat_type === 'private' && chat.value.members?.length > 0) {
      const otherMember = chat.value.members.find(m => m.user_id !== currentUserId.value)
      if (otherMember) {
        try {
          const userResponse = await api.get(`/users/${otherMember.user_id}`)
          chat.value.name = `${userResponse.data.first_name} ${userResponse.data.last_name}`
        } catch (error) {
          console.error('Load user error:', error)
        }
      }
    }
  } catch (error) {
    console.error('Load chat error:', error)
  }
}

async function loadMessages() {
  try {
    const response = await api.get(`/chats/${route.params.id}/messages`)
    messages.value = response.data
  } catch (error) {
    console.error('Load messages error:', error)
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || isSending.value) return
  
  isSending.value = true
  
  try {
    const messageData = {
      chat_id: parseInt(route.params.id),
      content: newMessage.value,
      message_type: 'text'
    }
    
    const response = await api.post('/messages', messageData)
    
    // Добавляем сообщение с анимацией
    const newMsg = { ...response.data, isNew: true }
    messages.value.push(newMsg)
    
    // Убираем флаг анимации через 500ms
    setTimeout(() => {
      const msg = messages.value.find(m => m.id === newMsg.id)
      if (msg) msg.isNew = false
    }, 500)
    
    newMessage.value = ''
    
    // Сбрасываем высоту textarea
    if (messageInput.value) {
      messageInput.value.style.height = 'auto'
    }
    
    // Принудительная прокрутка вниз
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Send message error:', error)
    alert('Ошибка отправки сообщения')
  } finally {
    isSending.value = false
  }
}

// Редактирование сообщения
function startEditMessage(message) {
  // Проверяем, не является ли сообщение пересланным
  if (message.content && message.content.startsWith('📩 Переслано:')) {
    alert('Пересланные сообщения нельзя редактировать')
    return
  }
  
  editingMessage.value = message
  newMessage.value = message.content
  messageInput.value?.focus()
}

function cancelEdit() {
  editingMessage.value = null
  newMessage.value = ''
}

async function updateMessage() {
  if (!newMessage.value.trim() || !editingMessage.value) return
  
  try {
    await api.put(`/messages/${editingMessage.value.id}`, {
      content: newMessage.value
    })
    
    // Обновляем сообщение локально
    const msg = messages.value.find(m => m.id === editingMessage.value.id)
    if (msg) {
      msg.content = newMessage.value
      msg.isEdited = true
    }
    
    cancelEdit()
  } catch (error) {
    console.error('Update message error:', error)
    alert('Ошибка редактирования сообщения')
  }
}

// Удаление сообщения
async function deleteMessage(messageId) {
  if (!confirm('Удалить сообщение?')) return
  
  try {
    await api.delete(`/messages/${messageId}`)
    messages.value = messages.value.filter(m => m.id !== messageId)
  } catch (error) {
    console.error('Delete message error:', error)
    alert('Ошибка удаления сообщения')
  }
}

// Пересылка сообщения
async function startForwardMessage(message) {
  forwardingMessage.value = message
  
  // Загружаем список чатов
  try {
    const response = await api.get('/chats')
    availableChats.value = response.data.filter(c => c.id !== parseInt(route.params.id))
    showForwardModal.value = true
  } catch (error) {
    console.error('Load chats error:', error)
    alert('Ошибка загрузки чатов')
  }
}

async function forwardToChat(chatId) {
  if (!forwardingMessage.value) return
  
  try {
    await api.post('/messages', {
      chat_id: chatId,
      content: `📩 Переслано: ${forwardingMessage.value.content}`,
      message_type: 'text'
    })
    
    showForwardModal.value = false
    forwardingMessage.value = null
    alert('Сообщение переслано')
  } catch (error) {
    console.error('Forward message error:', error)
    alert('Ошибка пересылки сообщения')
  }
}



function onEmojiSelect(event) {
  newMessage.value += event.detail.unicode
  showEmojiPicker.value = false
}

let mediaRecorder = null
let audioChunks = []

async function startRecording() {
  try {
    // Запрашиваем доступ к микрофону
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }
    
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      await uploadAudioMessage(audioBlob)
      
      // Останавливаем все треки
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.start()
    isRecording.value = true
  } catch (error) {
    console.error('Error starting recording:', error)
    alert('Ошибка доступа к микрофону. Проверьте разрешения браузера.')
  }
}

function stopRecording() {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
  }
}

async function uploadAudioMessage(audioBlob) {
  try {
    const formData = new FormData()
    formData.append('file', audioBlob, 'voice-message.webm')
    
    const uploadResponse = await api.post('/messages/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    const messageData = {
      chat_id: parseInt(route.params.id),
      content: '🎤 Голосовое сообщение',
      message_type: 'audio',
      attachment: {
        file_name: 'voice-message.webm',
        file_path: uploadResponse.data.file_path,
        file_type: 'audio/webm',
        file_size: audioBlob.size
      }
    }
    
    await api.post('/messages', messageData)
    await loadMessages()
    scrollToBottom()
  } catch (error) {
    console.error('Upload audio error:', error)
    alert('Ошибка отправки голосового сообщения')
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

async function clearChatHistory() {
  if (!confirm('Вы уверены, что хотите очистить историю чата? Это действие нельзя отменить.')) {
    return
  }
  
  try {
    await api.delete(`/chats/${route.params.id}/messages`)
    messages.value = []
    alert('История чата очищена')
  } catch (error) {
    console.error('Clear chat error:', error)
    alert('Ошибка очистки чата')
  }
}

async function renameChatPrompt() {
  const newName = prompt('Введите новое название чата:', chat.value?.name || '')
  
  if (!newName || newName === chat.value?.name) {
    return
  }
  
  try {
    await api.put(`/chats/${route.params.id}`, { name: newName })
    await loadChat()
    alert('Чат переименован')
  } catch (error) {
    console.error('Rename chat error:', error)
    alert('Ошибка переименования чата')
  }
}

async function deleteChat() {
  if (!confirm('Вы уверены, что хотите удалить этот чат? Все сообщения будут удалены безвозвратно.')) {
    return
  }
  
  try {
    await api.delete(`/chats/${route.params.id}/`)
    alert('Чат удален')
    router.push('/chats')
  } catch (error) {
    console.error('Delete chat error:', error)
    const errorMessage = error.response?.data?.detail || error.message
    alert('Ошибка удаления чата: ' + errorMessage)
  }
}

function handleLeftGroup() {
  alert('Вы покинули группу')
  router.push('/chats')
}

function goToUserProfile() {
  // Для личных чатов переходим на профиль собеседника
  if (chat.value?.chat_type === 'private' && chat.value?.members?.length > 0) {
    // Находим собеседника (не текущего пользователя)
    const otherMember = chat.value.members.find(m => m.user_id !== currentUserId.value)
    if (otherMember) {
      router.push(`/users/${otherMember.user_id}`)
    }
  }
}

function adjustTextareaHeight() {
  const textarea = messageInput.value
  if (textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px'
  }
}

let typingTimeout = null
let isCurrentlyTyping = false

function handleTyping() {
  adjustTextareaHeight()
  
  // Отправляем индикатор "печатает" через WebSocket
  if (!isCurrentlyTyping && newMessage.value.trim()) {
    sendTyping(true)
    isCurrentlyTyping = true
  }
  
  // Сбрасываем таймер
  if (typingTimeout) {
    clearTimeout(typingTimeout)
  }
  
  // Через 3 секунды отправляем "перестал печатать"
  typingTimeout = setTimeout(() => {
    if (isCurrentlyTyping) {
      sendTyping(false)
      isCurrentlyTyping = false
    }
  }, 3000)
}

function showReactionPicker(messageId) {
  selectedMessageForReaction.value = selectedMessageForReaction.value === messageId ? null : messageId
}

function closeReactionPicker() {
  selectedMessageForReaction.value = null
}

async function addReaction(messageId, emoji) {
  try {
    // В будущем отправить на сервер
    // await api.post(`/messages/${messageId}/reactions`, { emoji })
    
    // Временно добавляем локально
    const message = messages.value.find(m => m.id === messageId)
    if (message) {
      if (!message.reactions) {
        message.reactions = []
      }
      
      const existingReaction = message.reactions.find(r => r.emoji === emoji)
      if (existingReaction) {
        existingReaction.count++
      } else {
        message.reactions.push({ emoji, count: 1 })
      }
    }
    
    selectedMessageForReaction.value = null
  } catch (error) {
    console.error('Add reaction error:', error)
  }
}

function formatTime(dateStr) {
  return new Date(dateStr).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function markMessagesAsRead() {
  try {
    await api.post(`/chats/${route.params.id}/mark-read`)
  } catch (error) {
    console.error('Mark messages as read error:', error)
  }
}

function openDocument(attachment) {
  const fileUrl = `http://localhost:8000${attachment.file_path}`
  const fileName = attachment.file_name
  
  // Проверяем, поддерживается ли просмотр
  const supportedExtensions = ['.pdf', '.doc', '.docx']
  const isSupported = supportedExtensions.some(ext => fileName.toLowerCase().endsWith(ext))
  
  if (isSupported) {
    selectedDocument.value = {
      url: fileUrl,
      name: fileName
    }
    showDocumentViewer.value = true
  } else {
    // Для неподдерживаемых файлов открываем в новой вкладке
    window.open(fileUrl, '_blank')
  }
}

function closeDocumentViewer() {
  showDocumentViewer.value = false
  selectedDocument.value = { url: '', name: '' }
}

// Search functions
async function handleSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }
  
  searchTimeout = setTimeout(async () => {
    try {
      const response = await api.get('/messages/search', {
        params: {
          query: searchQuery.value,
          chat_id: route.params.id
        }
      })
      searchResults.value = response.data
    } catch (error) {
      console.error('Search error:', error)
    }
  }, 300)
}

function scrollToMessage(messageId) {
  const element = document.getElementById(`message-${messageId}`)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    element.classList.add('bg-yellow-100', 'dark:bg-yellow-900')
    setTimeout(() => {
      element.classList.remove('bg-yellow-100', 'dark:bg-yellow-900')
    }, 2000)
  }
  showSearch.value = false
}

// Sound functions
const isChatMuted = computed(() => {
  return soundSettings.value.mutedChats.includes(parseInt(route.params.id))
})

function toggleChatSound() {
  const chatId = parseInt(route.params.id)
  const index = soundSettings.value.mutedChats.indexOf(chatId)
  
  if (index > -1) {
    soundSettings.value.mutedChats.splice(index, 1)
  } else {
    soundSettings.value.mutedChats.push(chatId)
  }
  
  saveSoundSettings()
}

// Pinned messages functions
async function loadPinnedMessages() {
  try {
    const response = await api.get(`/messages/chat/${route.params.id}/pinned`)
    pinnedMessages.value = response.data
  } catch (error) {
    console.error('Load pinned messages error:', error)
  }
}

async function togglePinMessage(message) {
  try {
    if (message.is_pinned) {
      await api.delete(`/messages/${message.id}/pin`)
      message.is_pinned = false
    } else {
      await api.post(`/messages/${message.id}/pin`)
      message.is_pinned = true
    }
    await loadPinnedMessages()
  } catch (error) {
    console.error('Toggle pin error:', error)
    alert('Ошибка при закреплении сообщения')
  }
}
</script>

<style scoped>
@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}

@keyframes pulse-scale {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.animate-pulse-scale {
  animation: pulse-scale 0.5s ease-in-out;
}
</style>
