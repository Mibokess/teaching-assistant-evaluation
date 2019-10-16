<template>
    <div>
        <h2 class="mt-4">{{ lecture.name }}</h2>
        <div v-if="lecture.assistants == null">No assistants have been added for this course.</div>
        <ul v-else class="list-group border-0">

            <li class="list-group-item border-0" v-for="(a, index) in lecture.assistants" v-bind:key="a.id">
                <div class="accordion" id="accordionExample">
                    <div class="card mx-auto" style="max-width: 40rem">
                        <div class="card-header px-0 py-2" :id="'heading' + index" data-toggle="collapse"
                             :data-target="'#collapse' + index" aria-expanded="false"
                             :aria-controls="'collapse' + index">

                            <div class="d-flex flex-row justify-content-between">
                                <div class="mx-4" style="text-align: left">
                                    <span class="card-text-big">{{ a.name }}</span>
                                </div>
                                <div class="d-flex flex-row">
                                  <div class="mx-2" style="text-align:left" v-if="getDifficulty(a) >= 0.7">
                                    <i class="card-trophy fas fa-weight-hanging"></i>
                                  </div>
                                  <div class="mx-2" v-else-if="getDifficulty(a) <= 0.3">
                                    <i class="card-trophy fas fa-feather"></i>
                                  </div>
                                  <div class="mx-2" v-if="getInteractivity(a) >= 0.7">
                                    <i class="card-trophy fas fa-comments"></i>
                                  </div>
                                  <div class="mx-2" v-if="getInteractivity(a) <= 0.3">
                                    <i class="card-trophy fas fa-pen"></i>
                                  </div>
                                  <div class="mx-2" v-if="getSessionStyle(a) >= 0.7">
                                    <i class="card-trophy fas fa-dumbbell"></i>
                                  </div>
                                  <div class="mx-2" v-if="getSessionStyle(a) <= 0.3">
                                    <i class="card-trophy fas fa-chalkboard-teacher"></i>
                                  </div>
                                </div>
                                <div class="col" style="text-align: right">
                                    <router-link :to="{name: 'survey', params: {Sid:a.session.id}}"><span
                                            class="card-survey-link">
                                <i class="fas fa-vote-yea"></i></span></router-link>
                                </div>
                            </div>
                        </div>

                        <div :id="'collapse' + index" class="collapse" aria-labelledby="'heading' + index"
                             data-parent="#accordionExample">
                            <div class="card-body">
                                <Score description="Difficulty" left="fas fa-feather" right="fas fa-weight-hanging"
                                       v-bind:avg="getDifficulty(a)">
                                </Score>

                                <Score description="Interactivity" left="fas fa-pen" right="fas fa-comments"
                                       v-bind:avg="getInteractivity(a)">
                                </Score>

                                <Score description="Session Style" left="fas fa-chalkboard-teacher" right="fas fa-dumbbell"
                                       v-bind:avg="getSessionStyle(a)">
                                </Score>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
  import axios from 'axios'
  import Card from './Card.vue';
  import Score from './Score.vue';

  export default {
    name: 'Lecture',
    components: {
      Card,
      Score
    },
    data() {
      return {
        lecture: {
          id: null,
          name: null,
          description: null,
          assistants: [],
        },
        questionScores: [{}]
      }
    },
    methods: {
      getQuestionsScores: function(assistant) {
        return this.questionScores.filter(questionScore => questionScore.id == assistant.id)[0]
      },
      getScoreForQuestion(questionScores, id) {
        return questionScores.scores.filter(question => question.id == id)[0];
      },
      getDifficulty(assistant) {
        let questionScores = this.getQuestionsScores(assistant);

        let speedScore = this.getScoreForQuestion(questionScores, 3);
        let additionalScore = this.getScoreForQuestion(questionScores, 4);
        let comparisonScore = this.getScoreForQuestion(questionScores, 5);

        if ((speedScore.total + additionalScore.total + comparisonScore.total) == 0) return 0.5; 
        return (speedScore.score + additionalScore.score + comparisonScore.score) / (speedScore.total + additionalScore.total + comparisonScore.total)
      },
      getInteractivity(assistant) {
        let questionScores = this.getQuestionsScores(assistant);

        let questionScore = this.getScoreForQuestion(questionScores, 6);
        let discussionScore = this.getScoreForQuestion(questionScores, 7);
        let noteScore = this.getScoreForQuestion(questionScores, 8);

        if ((questionScore.total + discussionScore.total + noteScore.total) == 0) return 0.5; 
        return (questionScore.score + discussionScore.score + noteScore.score) / (questionScore.total + discussionScore.total + noteScore.total)
      },
      getSessionStyle(assistant) {
        let questionScores = this.getQuestionsScores(assistant);

        let exerciseScore = this.getScoreForQuestion(questionScores, 9);
        let differentScore = this.getScoreForQuestion(questionScores, 10);
        let solutionScore = this.getScoreForQuestion(questionScores, 11);

        if ((exerciseScore.total + differentScore.total + solutionScore.total) == 0) return 0.5; 
        return (exerciseScore.score + differentScore.score + solutionScore.score) / (exerciseScore.total + differentScore.total + solutionScore.total)
      }
    },
    mounted() {
      axios.get("/api/lectures/" + this.$route.params.Lid + "/?format=json")
        .then(currentLecture => {

          this.lecture.name = currentLecture.data.name;
          this.lecture.id = currentLecture.data.id;
        });

      axios.get("/api/questions/?format=json")
        .then(questions => {
          axios.get("/api/tas/?format=json")
            .then(tas => {
              axios.get("/api/sessions/?format=json")
                .then(sessions => {
                  axios.get("/api/votes/?format=json")
                    .then(votes => {
                      const sessionId = this.$route.params.Lid;
                      const lecturesData = [sessionId];
                      const questionsData = questions.data;
                      const tasData = tas.data;
                      const sessionsData = sessions.data;
                      const votesData = votes.data;

                      var results = [];

                      for (var i = 0; i < lecturesData.length; i++) {
                        for (var j = 0; j < tasData.length; j++) {
                          for (var k = 0; k < sessionsData.length; k++) {
                            const lectureIdem = lecturesData[i];
                            const tasItem = tasData[j];
                            const sessionItem = sessionsData[k];
                            const item = [lectureIdem, tasItem, sessionItem];
                            results.push(item);
                          }
                        }
                      }

                      function transform(element) {
                        const lectureItem = element[0];
                        const tasItem = element[1];
                        const sessionItem = element[2];
                        return {
                          "id": tasItem.id,
                          "name": tasItem.name,
                          "languages": [tasItem.language],
                          "session": sessionItem,
                          "votings": [
                            {"id": 1, "speed": 1},
                            {"id": 2, "speed": 0},
                            {"id": 3, "speed": 1},
                            {"id": 4, "speed": 1}
                          ],
                          "ratings": [
                            {"name": 'Speed', "average": 5.2},
                            {"name": 'Fluency', "average": 6.4},
                            {"name": 'Theoretical', "average": 2.7},
                          ]
                        }
                      }

                      const all = results
                        .filter(element => element[0] == element[2].lecture)
                        .filter(element => element[1].id == element[2].assistant)
                        .map(transform);

                      //this.lecture.name = JSON.stringify(all)
                      this.lecture.assistants = all;

                      var questionScoresArray = [];

                      all.forEach(function (assistant) {

                        console.log("votesData " + JSON.stringify(votesData));
                        console.log("assistant " + JSON.stringify(assistant));

                        let votesBelongingToSession = votesData.filter(vote => assistant.session.id == vote.session);

                        console.log("votesBelonging to Session" + JSON.stringify(votesBelongingToSession));

                        let questionScoresForAssistant = [];

                        console.log("votes " + sessionId + JSON.stringify(votesBelongingToSession));

                        questionsData.forEach(function (question) {
                          let votesBelongingToQuestion = votesBelongingToSession.filter(vote => vote.question == question.id);
                          let numberOfVotesPerQuestion = votesBelongingToQuestion.length;

                          let questionScore = 0;
                          votesBelongingToQuestion.forEach(function (vote) {
                            if (vote.opinion === "P") {
                              questionScore += 1;
                            }
                          });
                          questionScoresForAssistant.push({
                            "id":question.id,
                            "score":questionScore,
                            "total":numberOfVotesPerQuestion,
                          });
                        });

                        questionScoresArray.push({
                          id: assistant.id,
                          scores: questionScoresForAssistant
                        });
                      });
                      this.questionScores = questionScoresArray;
                    });
                })
            })
        })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">

    @import '../assets/App.styl'

    .accordion
        border-radius border-round

    .btn-rate
        margin-top 10px

    .card-survey-link
        color color3
        position relative
        top 6px
        right 10px

        &:hover
            color color4

    .card-trophy
      color color4
      position relative
      top 6px
      right 10px

      &:hover
          color color4


</style> 
