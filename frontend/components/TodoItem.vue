<template>
  <v-main>
    <v-container>
  <v-card id="app" color="rgb(0, 0, 0, 0.2)" elevation="7">
    <v-card-title class="pb-3" style="overflow-wrap: break-word;">
      <b>{{ todo.title }}</b>
      <v-spacer />
      <v-btn
        @click="remove"
        flat
        small
        icon
        style="position: absolute; right: 0; top: 0"
      >
        <v-icon :disabled="$nuxt.isServer" small>mdi-close</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text class="pb-3">
      <v-layout row justyfy-center align-center>
        <v-flex xs11 style="overflow-wrap: break-word;">
          {{ todo.text }}
        </v-flex>
        <v-flex xs1>
          <div style="text-align: right;">
            <v-checkbox
              v-model="todo.done"
              @click.once="toggle"
              hide-details
              class="pa-0 ma-0"
              style="display: inline-block;"
              color="green dark-1"
            />
          </div>
        </v-flex>
      </v-layout>
    </v-card-text>
    <v-card-actions>
      <span class="grey--text">
       <v-icon small>mdi-checkbox-marked-circle-outline</v-icon>  Выполнить до  {{ todo.dueDate }} | Создано
        <v-icon small>mdi-calendar-today</v-icon> {{ todo.createdDate }}
      </span>
      <v-spacer />
      <span class="grey--text">
        <v-icon small>mdi-hand-pointing-right</v-icon>Категория: {{ todo.category.name }}
      </span>
    </v-card-actions>
  </v-card>
  </v-banner>
    </v-container>
  </v-main>
</template>

<script>
import { GET_TODO_LIST, REMOVE_TODO, TOGGLE_TODO } from '../graphql'

export default {
  name: 'TodoItem',
  props: {
    todo: {
      type: Object,
      default: () => ({})
    }
  },
  methods: {
    toggle() {
      this.$apollo.mutate({
        mutation: TOGGLE_TODO,
        variables: {
          todoId: this.todo.id
        }
      })
    },
    remove() {
      const todoId = this.todo.id
      this.$apollo.mutate({
        mutation: REMOVE_TODO,
        variables: {
          todoId
        },
        update(store, {data: { removeTodo } }) {
          if (!removeTodo) return
          const data = store.readQuery({ query: GET_TODO_LIST })
          data.todoList = data.todoList.filter(todo => todo.id !== todoId)
          store.writeQuery({ query: GET_TODO_LIST, data })
        }
      })
    }
  }
}
</script>

<style>
#app {
  background: url('https://ohlaladani.com.br/wp-content/uploads/wallpaper-OHLALADANI_DESKTOP_WALLPAPERS_AVENTURA-2.jpg')
    no-repeat center center fixed !important;
  background-size: cover;
}
</style>
