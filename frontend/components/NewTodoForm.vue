<template>
  <v-main>
    <v-container>
  <v-form ref="form" v-model="valid">
    <v-card elevation="12">
      <v-card-text class="pt-0 mt-7">
        <v-layout row wrap>
          <v-flex xs8>
            <!--Поле ввода имени задачи-->

            <v-text-field
              v-model="newTodo.title"
              :rules="[nonEmptyField]"
              label="Задача"
              prepend-icon="mdi-lightbulb-outline"
            />
          </v-flex>
          <v-flex xs4>
            <!--Поле выбора даты выполнения задачи-->
            <v-menu
              ref="menu"
              v-model="menu"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="newTodo.dueDate"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              min-width="290px"
              >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="newTodo.dueDate"
                  :rules="[nonEmptyField]"
                  v-on="on"
                  label="Дата выполнения"
                  readonly
                  prepend-icon="mdi-calendar-today"
                  />
              </template>
              <v-date-picker
                v-model="newTodo.dueDate"
                no-title
                scrollable
                locale="ru-ru"
                first-day-of-week="1">
                <v-spacer />
                <v-btn @click="menu = false" flat color="secondary">Отмена</v-btn>
                <v-btn
                  @click="$refs.menu.save(newTodo.dueDate)"
                  flat
                  color="primary"
                  >Выбрать</v-btn
                >
              </v-date-picker>
            </v-menu>
          </v-flex>
          <v-flex xs12>
            <v-textarea
              v-model="newTodo.text"
              label="Описание"
              hide-details
              rows="1"
              class="py-0 my-0"
              prepend-icon="mdi-information-outline"

            />
          </v-flex>
        </v-layout>
      </v-card-text>
      <v-card-actions>
        <!-- Селектор категорий. Позволяет добавлять несуществующие позиции -->
        <v-combobox
          v-model="newTodo.category"
          :rules="[nonEmptyField]"
          :items="categories"
          hide-details
          label="Категория"
          class="my-0 mx-2 mb-2 pt-3"
          prepend-icon="mdi-hand-pointing-right"
        />
        <v-spacer />
        <v-btn :disabled="!valid" @click="add" color="blue lighten-3" flat
          >Добавить</v-btn
        >
        </v-card-actions>
      </v-card>
    </v-form>
      </v-container>
    </v-main>
</template>

<script>
// импортируем свеженаписанные запросы
import { ADD_TODO, GET_CATEGORIES, GET_TODO_LIST } from '../graphql'

export default {
  name: 'NewTodoForm',
  data() {
    return {
      newTodo: null,
      categories: ['home', 'work'],
      valid: false,
      menu: false,
      nonEmptyField: text =>
        text ? !!text.length : 'Поле не должно быть пустым',
      loading: false // индикация выполнения запроса
    }
  },
  apollo: {
    // загрузка данных для селектора категорий
    categories: {
      query: GET_CATEGORIES,
      update({ categories }) {
        return categories.map(c => c.name)
      }
    }
  },
  created() {
    this.clear()
  },
  methods: {
    add() {
      this.loading = true
      this.$apollo
        .mutate({
          mutation: ADD_TODO,
          variables: {
            ...this.newTodo
          },
          // кэш аполло позволяет манипулировать данными из этого кэша, вне зависимости
          // от того, в каком компоненте выполняется код. Здесь в качестве ответа
          // сервера мы получаем новую запись Todo. Добавляем её в кэш, записываем
          // обратно по запросу GET_TODO_LIST, таким образом переменная Apollo
          // сам разошлет всем подписчикам данного запроса измененные данные. В нашем
          // случае подписчиком является переменная todoList в компоненте index.vue
          update: (store, { data: { addTodo } }) => {
            // если в кэше отсутствуют данные по запросу, то бросится исключение
            const todoListData = store.readQuery({ query: GET_TODO_LIST })
            todoListData.todoList.unshift(addTodo)
            store.writeQuery({ query: GET_CATEGORIES, data: todoListData })

            const categoriesData = store.readQuery({ query: GET_CATEGORIES })
            // В списке категорий ищем категорию новой записи Todo. При неудачном поиске
            // добавляем в кэш. Таким образом селектор категорий всегда остается
            // в актуальном состоянии
            const category = categoriesData.categories.find(
              c => c.name === addTodo.category.name
            )
            if (!category) {
              categoriesData.categories.push(addTodo.category)
              store.writeQuery({ query: GET_CATEGORIES, data: categoriesData })
            }
          }
        })
        .then(() => {
          this.clear()
          this.loading = false
          this.$refs.form.reset() // сброс валидации формы
        })
    },
    clear() {
      this.newTodo = {
        title: '',
        text: '',
        dueDate: '',
        category: ''
      }
    }
  }
}
</script>

<style>
#app {
  background: url('https://images.wallpaperscraft.ru/image/ptitsa_nebo_gradient_125987_1920x1080.jpg')
    no-repeat center center fixed !important;
  background-size: cover;
}
</style>



