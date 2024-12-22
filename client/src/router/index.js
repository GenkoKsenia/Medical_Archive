import { createRouter, createWebHistory } from 'vue-router'
import PatientView from '@/components/PatientView.vue'
import MedicinesView from '@/components/MedicinesView.vue'
import DoctorsView from '@/components/DoctorsView.vue'
import ReleaseFormsView from '@/components/ReleaseFormsView.vue'
import TherapeuticActionsView from '@/components/TherapeuticActionsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      {
        path: "/patients",
        name: PatientView,
        component: PatientView
      },
      {
        path: "/medicins",
        name: MedicinesView,
        component: MedicinesView
      },
      {
        path: "/doctors",
        name: DoctorsView,
        component: DoctorsView
      },
      {
        path: "/releaseForms",
        name: ReleaseFormsView,
        component: ReleaseFormsView
      },
      {
        path: "/therapeuticActions",
        name: TherapeuticActionsView,
        component: TherapeuticActionsView
      },
  ]
})

export default router
