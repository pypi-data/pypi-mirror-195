export default {
  meta: {
    inMenu: true,
    titleKey: "evalu.menu_title",
    icon: "mdi-forum-outline",
    permission: "evalu.view_menu_rule",
  },
  props: {
    byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
  },
  children: [
    {
      path: "parts/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationParts",
      meta: {
        inMenu: true,
        titleKey: "evalu.parts.menu_title",
        icon: "mdi-format-list-bulleted-type",
        permission: "evalu.view_evaluation_parts",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "parts/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.createEvaluationPart",
    },
    {
      path: "parts/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.editEvaluationPart",
    },
    {
      path: "parts/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.deleteEvaluationPart",
    },
    {
      path: "phases/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationPhases",
      meta: {
        inMenu: true,
        titleKey: "evalu.phases.menu_title",
        icon: "mdi-calendar-range-outline",
        permission: "evalu.view_evaluation_phases",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "phases/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.createEvaluationPhase",
    },
    {
      path: "phases/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationPhase",
    },
    {
      path: "phases/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.editEvaluationPhase",
    },
    {
      path: "phases/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.deleteEvaluationPhase",
    },
    {
      path: "phases/:pk/deletion/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.deleteDataFromPhase",
    },
    {
      path: "evaluations/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationPhasesOverview",
      meta: {
        inMenu: true,
        titleKey: "evalu.evaluation.all_menu_title",
        icon: "mdi-format-list-checks",
        permission: "evalu.view_evaluationphases_overview_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "evaluations/:pk/register/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.registerForEvaluation",
    },
    {
      path: "evaluations/registrations/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationRegistration",
    },
    {
      path: "evaluations/registrations/:pk/manage/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.manageEvaluationProcess",
    },
    {
      path: "evaluations/groups/:pk/start/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.startEvaluationForGroup",
    },
    {
      path: "evaluations/groups/:pk/stop/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.stopEvaluationForGroup",
    },
    {
      path: "evaluations/registrations/:pk/finish/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.finishEvaluation",
    },
    {
      path: "evaluations/registrations/:pk/results/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationResults",
    },
    {
      path: "evaluations/registrations/:pk/results/pdf/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationResultsAsPdf",
    },
    {
      path: "evaluations/evaluate/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluationsAsParticipant",
      meta: {
        inMenu: true,
        titleKey: "evalu.evaluation.my_menu_title",
        icon: "mdi-comment-quote-outline",
        permission: "evalu.view_evaluations_as_participant_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "evaluations/evaluate/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "evalu.evaluatePerson",
    },
  ],
};
