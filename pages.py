from flask import Flask, render_template, redirect, url_for
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
import base64

app = Flask(__name__)

#just for testing, I'm going to have global states

# wins for both pages
global a
a = np.load("wins.npy")

#losses for both pages
global b
b = np.load("loses.npy")



@app.route('/')
def index():
	np.save("wins.npy",a)
	np.save("loses.npy",b)
	fig1 = get_figure(0)
	fig2 = get_figure(1)
	return render_template("index.html", states=zip(a,b), fig1=fig1, fig2=fig2)

@app.route('/reset/')
def reset():
	np.save("wins.npy",[1,1])
	np.save("loses.npy",[1,1])
	global a
	a = np.load("wins.npy")
	global b
	b = np.load("loses.npy")
	return redirect(url_for('index'))

def get_figure(index):
	x = np.linspace(scipy.stats.beta.ppf(0.01, a[index], b[index]),scipy.stats.beta.ppf(0.99, a[index], b[index]), 100)
	plt.clf()
	plt.plot(x,scipy.stats.beta.pdf(x,a[index],b[index]))

	figfile = BytesIO()
	plt.savefig(figfile, format='png')
	figfile.seek(0)  # rewind to beginning of file
	figdata_png = base64.b64encode(figfile.getvalue())
	return figdata_png

@app.route('/page1/')
def first():
	results = get_figure(0)
	return render_template("page1.html", results=results)

@app.route('/page1/buy/')
def buy_first():
	a[0] += 1
	return redirect(url_for('index'))

@app.route('/page1/leave/')
def leave_first():
	b[0] += 1
	return redirect(url_for('index'))


@app.route('/page2/')
def second():
	results = get_figure(1)
	return render_template("page2.html", results=results)

@app.route('/page2/buy/')
def buy_second():
	a[1] += 1
	return redirect(url_for('index'))

@app.route('/page2/leave/')
def leave_second():
	b[1] += 1
	return redirect(url_for('index'))

@app.route('/random/')
def get_random():
	li = [scipy.stats.beta.rvs(i,j) for (i,j) in zip(a,b)] #draw from beta distribution
	val = np.argmax(np.array(li))
	if val == 0:
		return redirect(url_for('first'))
	elif val == 1:
		return redirect(url_for('second'))


# def thompson(self):
	# return np.argmax(np.array([self.J[i]*scipy.stats.beta.rvs(a,b) for i,(a,b) in enumerate(zip(self.a,self.b))]))


if __name__ == "__main__":
	app.run(debug=True)