<template>
  <div v-if="loading">
    <p>loading...</p>
  </div>
  <div v-else-if="errored">
    <p>Could not retrieve lectures</p>
  </div>
  <div v-else="">
    <div class="d-flex sticky-top" style="z-level: 2; padding: .75rem 1.25rem;">
      <div class="d-flex flex-row flex-grow-1 mx-auto badge-pill bg-color1 align-content-center" style="max-width: 30rem; padding: .25rem 1rem;">
        <input v-model="search" class="flex-grow-1 text-white" style="background: none; border: none; " type="text" placeholder="Search ...">
        <i class="fa fa-search"></i>
      </div>
    </div>
    <div class="fixed-top" style="height: 4.5rem; z-index: 1; "></div>
    <ul class="list-group border-0">
        <li class="list-group-item border-0" v-for="lecture in lectures.filter(l => this.searchResult.includes(l.id))" v-bind:key="lecture.id">          
          <div class="text-muted text-bold mx-auto my-2" style="max-width: 30rem" v-if="lecture.name=='Semester'">{{ lecture.year }} - {{ lecture.semester }}</div>
          <div v-else>
            <router-link :to="{name: 'lecture', params: {Lid:lecture.id}}">
                <Card>
                  <template v-slot:header></template>
                  <template v-slot:body>
                    <div class="row">
                      <span class="card-text-big text-left">{{ lecture.name }}</span>
                    </div>
                    <div class="row">
                      <i><span class="italic-color3 text-left">{{ lecture.professors }}</span></i>
                    </div>
                  </template>
                  <template v-slot:footer></template>
                </Card>  
          </router-link>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import Card from './Card.vue';
import * as Fuse from 'fuse.js';

export default {
  name: 'Lectures',
  components: {
    Card
  },
  props: {
  },
  data() {
    return {
      lectures: [
      ],
      errored: false,
      loading: true,
      search: '',
      searchResult: '',
      options: {
        keys: [{
          name: "name",
          weight: 0.7
        }, {
          name: "professors",
          weight: 0.3
        }],
        id: 'id'
      },
    }
  },
  watch: {
    search: function (newSearch, oldSearch) {
        this.searchResult = '🤔🤔🤔🤔🤔🤔';

        if (this.search) {
          this.getSearchResult();
        } else {
          this.searchResult = this.lectures.map(lecture => lecture.id);
        }
    },
  },

  methods: {
    getSearchResult: function() {
      var fuse = new Fuse(this.lectures, this.options);

      this.searchResult = fuse.search(this.search).map(result => Number(result)).filter(result => result >= 0);
    }
  },
  mounted() {
    axios.get("api/lectures?format=json")
      .then(res => {
        this.lectures = res.data;
        this.lectures.sort(function(firstLecture, secondLecture) {
          if (firstLecture.year < secondLecture.year || firstLecture.year == secondLecture.year && firstLecture.semester == 'HS') {
            return 1;
          }

          return -1;
        })

        let lastSemesterSeen = null;
        let lecturesWithSemesters = [];
        
        this.lectures.forEach(function (lecture) {
          if (lastSemesterSeen == null || lastSemesterSeen.localeCompare(lecture.semester) != 0) {
            lastSemesterSeen = lecture.semester;
            lecturesWithSemesters.push({ id: -1, name: 'Semester', year: lecture.year, semester: lecture.semester });
          } 

          lecturesWithSemesters.push(lecture);
        })

      this.lectures = Array.from(lecturesWithSemesters);
      this.searchResult = this.lectures.map(lecture => lecture.id);
    })
    .catch(err => {
    })
    .finally(() => this.loading = false)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">

@import '../assets/App.styl'

</style>
