<script setup>
import PatientView from './components/PatientView.vue';
import MedicinsView from './components/MedicinesView.vue';
</script>


<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse d-flex justify-content-center" style="margin-bottom: 30px; margin-top: 30px;" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <button class="btn btn-outline-success me-3" type="button">
              <router-link class="nav-link" to="/patients">
                Пациенты
              </router-link>
            </button>
            <button class="btn btn-outline-success me-3" type="button">
              <router-link class="nav-link" to="/medicins">
                Лекарства
              </router-link>
            </button>
            <button class="btn btn-outline-success me-3" type="button">
              <router-link class="nav-link" to="/doctors"> 
                Врачи 
              </router-link>
            </button>
            <button class="btn btn-outline-success me-3" type="button">
              <router-link class="nav-link" to="/releaseForms">
                Формы выпуска
              </router-link>
            </button>
            <button class="btn btn-outline-success me-3" type="button">
              <router-link class="nav-link" to="/therapeuticActions">
                Терапевтические действия
              </router-link>
            </button>
            
            <div class="btn-group">
              <button
                class="btn btn-secondary dropdown-toggle"
                type="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Войти
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админ</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="container">
      <router-view />
    </div>
  </div>
</template>



<style scoped></style>
