(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["pages-scanLogin-index"],{"92e6":function(t,i,n){"use strict";var e=n("4ea4");Object.defineProperty(i,"__esModule",{value:!0}),i.default=void 0,n("96cf");var a=e(n("1da1")),o=n("8cae"),r={data:function(){return{title:"Hello",loginUid:"",errorMsg:"",analysisData:{},loginData:{},userInfo:{}}},onLoad:function(t){var i=this;return(0,a.default)(regeneratorRuntime.mark((function n(){return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:t.login_uid?(i.loginUid=t.login_uid,i.getScanInfo()):uni.navigateTo({url:"/pages/index/index"});case 1:case"end":return n.stop()}}),n)})))()},methods:{getScanInfo:function(){var t=this;uni.request({url:o.API_URL+"api/dvadmin_third/login/get_scan_info/",data:{login_uid:this.loginUid},success:function(i){2e3!==i.data.code?t.errorMsg=i.data.msg:(t.analysisData=i.data.data.analysis_data,t.loginData=i.data.data.login_data),console.log(i.data)}})},confirmLogin:function(){var t=this;uni.request({url:o.API_URL+"api/dvadmin_third/confirm/confirm_login/",method:"post",header:{Authorization:"JWT "+uni.getStorageSync("token")},data:{login_uid:this.loginUid},success:function(i){2e3!==i.data.code?t.errorMsg=i.data.msg:(uni.showToast({title:"登录成功！"}),setTimeout((function(){uni.getStorageSync("is_webview")?webUni.navigateTo({url:"/pages/index/index"}):uni.navigateTo({type:"reLaunch",url:"/pages/index/index"})}),1500)),console.log(i.data)}})},cancel:function(){uni.getStorageSync("is_webview")?webUni.navigateTo({url:"/pages/index/index"}):uni.navigateTo({type:"reLaunch",url:"/pages/index/index"})}}};i.default=r},ce0f:function(t,i,n){var e=n("24fb");i=e(!1),i.push([t.i,".content[data-v-3abc4d0a]{\n  /* display: flex; */flex-direction:column;align-items:center;justify-content:center}.logo[data-v-3abc4d0a]{height:%?200?%;width:%?200?%;margin-top:%?150?%;margin-left:auto;margin-right:auto;margin-bottom:%?50?%}.text-area[data-v-3abc4d0a]{display:flex;justify-content:center}.title[data-v-3abc4d0a]{font-size:%?36?%;color:#8f8f94}uni-button[data-v-3abc4d0a]::after{border:none}",""]),t.exports=i},ddaf:function(t,i,n){"use strict";n.d(i,"b",(function(){return a})),n.d(i,"c",(function(){return o})),n.d(i,"a",(function(){return e}));var e={uniSection:n("17c6").default,uniList:n("da28").default,uniListItem:n("a855").default},a=function(){var t=this,i=t.$createElement,n=t._self._c||i;return n("v-uni-view",{staticClass:"content"},[n("cu-custom",{attrs:{bgColor:"bg-blue",isBack:!1}}),n("v-uni-view",{staticStyle:{"text-align":"center"}},[n("v-uni-image",{staticClass:"logo",attrs:{src:"/static/logo.png"}})],1),t.errorMsg?n("v-uni-view",{staticStyle:{"text-align":"center"}},[n("v-uni-text",{staticClass:"title"},[t._v("错误信息："+t._s(t.errorMsg))])],1):n("v-uni-view",[n("v-uni-view",{staticStyle:{"text-align":"center","margin-bottom":"30px"}},[n("v-uni-text",{staticStyle:{"font-size":"18px"}},[t._v("您正在登录，请确认是否是本人")])],1),n("uni-section",{attrs:{type:"line",title:""}},[n("uni-list",[n("uni-list-item",{attrs:{title:"登录省份",rightText:t.analysisData.province}}),n("uni-list-item",{attrs:{title:"登录城市",rightText:t.analysisData.city}}),n("uni-list-item",{attrs:{title:"登录ip",rightText:t.loginData.ip}}),n("uni-list-item",{attrs:{title:"登录设备",rightText:t.loginData.browser}})],1)],1),n("v-uni-view",{staticStyle:{margin:"20px","margin-top":"40px"}},[n("v-uni-button",{staticStyle:{"border-radius":"30px"},attrs:{type:"primary"},on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.confirmLogin.apply(void 0,arguments)}}},[t._v("确认登录")]),n("br"),n("v-uni-button",{staticStyle:{"border-radius":"30px"},attrs:{type:"default"},on:{click:function(i){arguments[0]=i=t.$handleEvent(i),t.cancel.apply(void 0,arguments)}}},[t._v("取消登录")])],1)],1)],1)},o=[]},ea9b:function(t,i,n){"use strict";n.r(i);var e=n("ddaf"),a=n("fb94");for(var o in a)"default"!==o&&function(t){n.d(i,t,(function(){return a[t]}))}(o);n("f810");var r,u=n("f0c5"),s=Object(u["a"])(a["default"],e["b"],e["c"],!1,null,"3abc4d0a",null,!1,e["a"],r);i["default"]=s.exports},f810:function(t,i,n){"use strict";var e=n("fa7c"),a=n.n(e);a.a},fa7c:function(t,i,n){var e=n("ce0f");"string"===typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);var a=n("4f06").default;a("46c5039e",e,!0,{sourceMap:!1,shadowMode:!1})},fb94:function(t,i,n){"use strict";n.r(i);var e=n("92e6"),a=n.n(e);for(var o in e)"default"!==o&&function(t){n.d(i,t,(function(){return e[t]}))}(o);i["default"]=a.a}}]);