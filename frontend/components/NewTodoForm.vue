<template>
  <v-form ref="form" v-model="valid">
    <v-card>
      <v-card-text class="pt-0 mt-0">
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
                  :rules="[nonemptyField]"
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
              :rules="[nonEmptyField]"
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
          class="my-0 mx-2 mb-2 pt-0"
          prepend-icon="mdi-hand-pointing-right"
        />
        <v-spacer />
        <v-btn :disabled="!valid" @click="add" color="blue lighten-1" flat
          >Добавить</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
export default {
  name: 'NewTodoForm',
  data() {
    return {
      newTodo: null,
      categories: ['Дом', 'Другое', 'Учеба'],
      valid: false,
      menu: false,
      nonEmptyField: text =>
        text ? !!text.length : 'Поле не должно быть пустым'
    }
  },
  created() {
    this.clear()
  },
  methods: {
    add() {
      this.$emit('add', this.newTodo)
      this.clear()
      this.$refs.form.reset()
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



