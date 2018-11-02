var koma_id = document.getElementById('koma_id').value;
var next_rand_id = document.getElementById('next_rand_id').value;

var app = new Vue({
  el: '#annotate',
  delimiters: ["[[", "]]"],
  data: {
    chara_num: 3,
    have_eyes_num: 0,
    koma_id: '',
    whos_str: '',
    grad_str: '',
    eyes_str: '',
    step: 1,
    grad_rad: 0,
    grad_list: ['左向き前', '右向き前', '正面前', '背面'],
    chara_list: ['ゆ', '縁', '唯', '母', '千', '佳', 'ふ', '他'],
    eyes_list: ['詳細', '隠れ', 'デフォルメ'],
  },
  mounted: function () {
    this.koma_id = koma_id
    this.chara_num = document.getElementById("chara_num").value
    this.whos_str = document.getElementById("whos").value
    this.grad_str = document.getElementById("face_direction").value
    this.eyes_str = document.getElementById("eyes").value
    this.step = document.getElementById("step").value
    if (this.eyes_str) {
      this.have_eyes_num = this.eyes_str.split(',').length - 1
    }
  },
  computed: {
    is_can_save: function() {
      // 簡単なバリデーション
      if (this.chara_num == 0) {
        // 0人
        var is_blank_fill_whos_and_grad = this.whos_str === '' && this.grad_str === ''
        var is_eyes_input_ok = this.eyes_str === '' && this.have_eyes_num === 0
        return is_blank_fill_whos_and_grad && is_eyes_input_ok
      } else {
        // 1人以上
        var is_fill_whos_and_grad = this.whos_str !== '' && this.grad_str !== ''
        var is_eyes_input_ok = (this.get_have_eyes_num() > 0 && this.eyes_str !== '') || this.get_have_eyes_num() === 0
        const is_ok_inputed_str = is_fill_whos_and_grad && is_eyes_input_ok

        var is_equall_chara_num_and_whos_len = Number(this.chara_num) === this.whos_str.split(',').length - 1
        var is_equall_grad_str_len_and_grad_str_len = this.have_eyes_num === this.eyes_str.split(',').length - 1
        const is_ok_str_length = is_equall_chara_num_and_whos_len && is_equall_grad_str_len_and_grad_str_len

        return is_ok_inputed_str && is_ok_str_length
      }
    },
    int_chara_num: function () {
      return Number(this.chara_num)
    },
    eyes_strc: function () {
      return this.eyes_str
    },
  },
  filters: {
    captionFormat: function (date) {
      var id_split = this.koma_id.split('-')
      return `${id_split[0]}巻${id_split[1]}ページ${id_split[2]}コマ目`
    }
  },
  directives: {
    focus: {
      // 画面読み込み時、要素にフォーカスするディレクティブ定義
      inserted: function (el) {
        console.log('focus',el)
        el.focus()
      }
    }
  },
  methods: {
    submit_0_chara_num: function() {
      this.reset_values(0)
      this.$nextTick(function() {
        this.submit_by_key()
      })
    },
    keymonitorCharaNum: function(event) {
      if (event.key === 'r') {
        window.location.href = '/annotate/' + next_rand_id + '?default_eye='
      } else if (event.key === 't') {
        window.location.href = '/annotate/' + next_rand_id
      } else {
        var elems = document.querySelectorAll(`[value='${event.key}']`)
        if (elems[0]) { elems[0].checked = true }
        this.chara_num = event.key
        if (this.chara_num === '0') {
          this.submit_by_key()
        }
        document.getElementById('rad0_whos').focus()
      }
    },
    keymonitorWho: function(event) {
      if (event.key === 'r') {
        window.location.href = '/annotate/' + next_rand_id
      } else if (event.key === 't') {
        window.location.href = '/annotate/' + next_rand_id
      } else if (event.key === 'Escape') {
        this.whos_str = ''
      } else if (event.key === 'q') {
        document.getElementById('rad_grad0-1').focus()
      } else {
        var who = this.chara_list[Number(event.key) - 1]
        var elems = document.querySelectorAll(`[value='${who}']`)
        if (elems[0]) {
          elems[0].checked = true
          this.whos_str = this.whos_str + who + ','
        }
      }
    },
    keymonitorGrad: function(event) {
      if (event.key === 'esc') {
        this.grad_str = ''
      } else if (event.key === 'q') {
        var elems = document.querySelectorAll(`[value='${eyes}']`)
        document.getElementById('rad0_eyes2').focus()
      } else if (event.key === 'e') {
        if (this.is_can_save) { this.submit_by_key() }
      } else if (event.key === 'r') {
        if (this.is_can_save) { this.submit_by_key() }
      } else {
        var grad = this.grad_list[Number(event.key) - 1]
        var elems = document.querySelectorAll(`[value='${grad}']`)
        this.grad_rad = (this.grad_rad % this.chara_num) + 1
        var select_q = `[value='${grad}'][name=grad-${this.grad_rad}]`
        document.querySelector(select_q).checked = true
        this.change_eyes_num()
      }
    },
    keymonitorEyes: function(event) {
      if (event.key === 'esc') {
        this.eyes_str = ''
      } else if (event.key === 'e') {
        if (this.is_can_save) { this.submit_by_key() }
      } else if (event.key === 'r') {
        if (this.is_can_save) { this.submit_by_key() }
      } else {
        var eyes = this.eyes_list[Number(event.key) - 1]
        console.log(eyes)
        var elems = document.querySelectorAll(`[value='${eyes}']`)
        console.log(elems)
        this.eyes_rad = (this.eyes_rad % this.have_eyes_num) + 1
        console.log(this.eyes_rad)
        var select_q = `[value='${eyes}'][name=eyes-${this.eyes_rad + 2}]`
        console.log(select_q)
        document.querySelector(select_q).checked = true
      }
    },
    submit_by_key: function() {
      var form = document.getElementById("annotate_form");
      var form = document.querySelector("[type=submit]") ;
      form.click()
    },
    get_have_eyes_num: function() {
      var ches = document.querySelectorAll("[type=radio]:checked")
      var have_eyes_num = 0
      for (var i=0; i< ches.length; i++) {
        if (ches[i].labels.length > 0) {
          var label_text = ches[i].labels[0].innerText
          label_text.indexOf('前') > 0 ? have_eyes_num++ : null
        }
      }
      return have_eyes_num
    },
    send_chara_num: function (elem) {
      var value = elem.target.labels[0].innerText
      if (Number(value) === 0) {
        this.reset_values(0)
      }
    },
    send_who_str: function (elem) {
      console.log('sws', elem)
      var value = elem.target.labels[0].innerText
      if (value && value.length == 1) {
        this.whos_str = this.whos_str + value + ','
      }
    },
    send_grad_or_eyes_str: function (kind) {
      var ches = document.querySelectorAll("[type=radio]:checked")
      var target_str = ''
      for (var i=0; i< ches.length; i++) {
        if(ches[i].id.indexOf(kind) > 0) {
          var label_text = ches[i].labels[0].innerText
          target_str = target_str + label_text + ','
        }
      }
      if (kind == 'grad') {
        this.grad_str = target_str
      } else if (kind == 'eyes') {
        this.eyes_str = target_str
      }
    },
    change_eyes_num: function () {
      this.have_eyes_num = this.get_have_eyes_num()

      this.send_grad_or_eyes_str('grad')
      this.$nextTick(function() {
        this.send_grad_or_eyes_str('eyes')
      })
    },
    reset_values: function (chara_num=1) {
      console.log('reset')
      this.chara_num = chara_num === 1 ? 1 : 0
      this.have_eyes_num = 0
      this.koma_id = koma_id
      this.whos_str = ''
      this.grad_str = ''
      this.eyes_str = ''
    },
    reset_who_value: function () {
      this.whos_str = ''
      document.getElementById('rad0_whos').focus()
    },
  },
})
