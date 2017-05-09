<template>
	<form id="msform" :model="registerForm">
		<!-- progressbar -->
		<ul id="progressbar">
			<li class="active">账号信息</li>
			<li>其他</li>
			<li>检查结果</li>
		</ul>
		<!-- fieldsets -->
		<fieldset>
			<h2 class="fs-title">注册你的账号</h2>
			<h3 class="fs-subtitle">第一步</h3>
			<input type="text" v-model='registerForm.username' name="username" placeholder="用户名" />
			<input type="text" v-model='registerForm.chinese_name' name="chinese_name" placeholder="真名" />
			<input type="password" v-model='registerForm.password' name="password" placeholder="Password" />
			<input type="password" name="password2" placeholder="Confirm Password" />
			<!--<input type="button" name="submit" class="next action-button" value="提交" />-->
			<el-button type="primary" @click="submitForm('registerForm')">注册</el-button>
		</fieldset>
		<!--<fieldset>
			<h2 class="fs-title">Social Profiles</h2>
			<h3 class="fs-subtitle">Your presence on the social network</h3>
					<input type="text" name="email" placeholder="Email" />
			<input type="text" name="twitter" placeholder="Twitter" />
			<input type="text" name="facebook" placeholder="Facebook" />
			<input type="text" name="gplus" placeholder="Google Plus" />
			<input type="button" name="previous" class="previous action-button" value="Previous" />
			<input type="button" name="next" class="next action-button" value="Next" />
		</fieldset>
		<fieldset>
			<h2 class="fs-title">Personal Details</h2>
			<h3 class="fs-subtitle">We will never sell it</h3>
			<input type="text" name="fname" placeholder="First Name" />
			<input type="text" name="lname" placeholder="Last Name" />
			<input type="text" name="phone" placeholder="Phone" />
			<textarea name="address" placeholder="Address"></textarea>
			<input type="button" name="previous" class="previous action-button" value="Previous" />
			<input type="submit" name="submit" class="submit action-button" value="Submit" />
		</fieldset>-->
	</form>
</template>

<script>
export default {
	data: function () {
		return {
			registerForm: {
				username: '',
				password: '',
				email: '',
			},
			rules: {
				username: [
					{ required: true, message: '请输入用户名', trigger: 'blur' }
				],
				password: [
					{ required: true, message: '请输入密码', trigger: 'blur' }
				]
			}
		}
	},
	methods: {
		submitForm(formName) {
			const self = this;
			let postdata = 'username=' + self.registerForm.username + '&password=' + self.registerForm.password;
			console.log(postdata);
			this.$axios.post('/accounts/register/', postdata).then((res) => {
				if (res.data.code == '0') {
					var sid = res.data.content;
					// localStorage.setItem('sid', sid);
					self.$router.push('/');
				} else {
					console.log('密码或者用户名错误');
					return false;
				}
			});
		},

		},
	
};

</script>

<style >
/*custom font*/

@import url(http://fonts.googleapis.com/css?family=Montserrat);


/*basic reset*/

* {
	margin: 0;
	padding: 0;
}

html {
	height: 100%;
	/*Image only BG fallback*/
	background: url('http://thecodeplayer.com/uploads/media/gs.png');
	/*background = gradient + image pattern combo*/
	background: linear-gradient(rgba(196, 102, 0, 0.2), rgba(155, 89, 182, 0.2)),
	url('http://thecodeplayer.com/uploads/media/gs.png');
}

body {
	font-family: montserrat, arial, verdana;
}


/*form styles*/

#msform {
	width: 400px;
	margin: 50px auto;
	text-align: center;
	position: relative;
}

#msform fieldset {
	background: white;
	border: 0 none;
	border-radius: 3px;
	box-shadow: 0 0 15px 1px rgba(0, 0, 0, 0.4);
	padding: 20px 30px;

	box-sizing: border-box;
	width: 80%;
	margin: 0 10%;

	/*stacking fieldsets above each other*/
	position: absolute;
}


/*Hide all except first fieldset*/

#msform fieldset:not(:first-of-type) {
	display: none;
}


/*inputs*/

#msform input,
#msform textarea {
	padding: 15px;
	border: 1px solid #ccc;
	border-radius: 3px;
	margin-bottom: 10px;
	width: 100%;
	box-sizing: border-box;
	font-family: montserrat;
	color: #2C3E50;
	font-size: 13px;
}


/*buttons*/

#msform .action-button {
	width: 100px;
	background: #27AE60;
	font-weight: bold;
	color: white;
	border: 0 none;
	border-radius: 1px;
	cursor: pointer;
	padding: 10px 5px;
	margin: 10px 5px;
}

#msform .action-button:hover,
#msform .action-button:focus {
	box-shadow: 0 0 0 2px white, 0 0 0 3px #27AE60;
}


/*headings*/

.fs-title {
	font-size: 15px;
	text-transform: uppercase;
	color: #2C3E50;
	margin-bottom: 10px;
}

.fs-subtitle {
	font-weight: normal;
	font-size: 13px;
	color: #666;
	margin-bottom: 20px;
}


/*progressbar*/

#progressbar {
	margin-bottom: 30px;
	overflow: hidden;
	/*CSS counters to number the steps*/
	counter-reset: step;
}

#progressbar li {
	list-style-type: none;
	color: white;
	text-transform: uppercase;
	font-size: 9px;
	width: 33.33%;
	float: left;
	position: relative;
}

#progressbar li:before {
	content: counter(step);
	counter-increment: step;
	width: 20px;
	line-height: 20px;
	display: block;
	font-size: 10px;
	color: #333;
	background: white;
	border-radius: 3px;
	margin: 0 auto 5px auto;
}


/*progressbar connectors*/

#progressbar li:after {
	content: '';
	width: 100%;
	height: 2px;
	background: white;
	position: absolute;
	left: -50%;
	top: 9px;
	z-index: -1;
	/*put it behind the numbers*/
}

#progressbar li:first-child:after {
	/*connector not needed before the first step*/
	content: none;
}


/*marking active/completed steps green*/


/*The number of the step and the connector before it = green*/

#progressbar li.active:before,
#progressbar li.active:after {
	background: #27AE60;
	color: white;
}
</style>
