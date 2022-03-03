<template>
  <div>
    <div id="captcha">
      <h1>拖动鼠标，旋转图像，还原字符</h1>
      <model-obj
        ref="model"
        src="/get_file"
        :controlsOptions="{ enablePan: false, enableZoom: false }"
        :lights="light"
        :backgroundColor="backgroundColor"
        :cameraPosition="camera"
        @on-click="OnClick"
      >
      </model-obj>
    </div>
    <div id="cap_result">
      <h2>验证{{ pass }}</h2>
    </div>
    <p id="github">
      恭喜验证通过~本项目的源码地址是
      <a href="https://github.com/sti1l-0/3D_captcha/tree/main/back_end">sti1l-0/3D_captcha</a>
    </p>
  </div>
</template>

<script>
import { ModelObj } from "vue-3d-model";

export default {
  data () {
    return {
      light: [
      ],
      pass: '不通过',
      backgroundColor: 0xffffff,
      camera: { x: 1, y: 1, z: 125 }
    }
  },
  mounted () {
    this.light = this.loadlight()
    this.backgroundColor = this.randomColor()
    var a = this.Radius125()
    this.camera.x = a[0]
    this.camera.y = a[1]
    this.camera.z = a[2]   
  },
  methods: {
    OnLoad() {
      //this.Radius125()
      requestAnimationFrame(function(){});
    },
    Radius125(){
        var a = Math.random() * 120 * (Math.round(Math.random())*2-1);
        var b = Math.random() * (125**2 - a**2)**0.5 * (Math.round(Math.random())*2-1);
        var c = (125**2 - a**2 - b**2)**0.5 * (Math.round(Math.random())*2-1)
        return [a,b,c]
    },
    loadlight(){
      return [
        {
          type: 'DirectionalLight', 
          position: { x: 1, y: 1, z: 1 }, 
          color: this.randomColor(), 
          intensity: 0.9, 
        },
        {
          type: 'DirectionalLight', 
          position: { x: 1, y: -1, z: -1 }, 
          color: this.randomColor(), 
          intensity: 0.9, 
        },
        {
          type: 'DirectionalLight', 
          position: { x: -1, y: -1, z: 1 }, 
          color: this.randomColor(), 
          intensity: 0.9, 
        },
        {
          type: 'DirectionalLight', 
          position: { x: -1, y: 1, z: -1 }, 
          color: this.randomColor(), 
          intensity: 0.9, 
        },
      ]
    },
    randomColor(){
      return Math.floor(Math.random()*16777215); 
    },
    OnClick() {
      this.$axios
        .post("/check", {
          posx: this.$refs.model.camera.position.x,
          posy: this.$refs.model.camera.position.y,
          posz: this.$refs.model.camera.position.z
        })
        .then((response) => {
          this.pass = String(response.data)=='true'?'通过':'不通过'
          if(this.pass === '通过'){
            var t = document.getElementById('captcha');//选取id为test的元素
            t.style.display = 'none';	// 隐藏选择的元素
            t = document.getElementById('cap_result');
            t.style.background = "green";
            t = document.getElementById('github');//选取id为test的元素
            t.style.visibility = 'visible';	// 隐藏选择的元素
          }
        });
    },
  },
  components: {
    ModelObj,
  },
};
</script>

<style scoped>
  #captcha {
    height: 40%;
    width: 40%;
  }
  #cap_result {
    background: red;
    width: fit-content;
  }

  #github{
    visibility: hidden;
}
</style>