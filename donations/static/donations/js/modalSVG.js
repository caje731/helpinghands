var bezier = function(x1, y1, x2, y2, epsilon){

	var curveX = function(t){
		var v = 1 - t;
		return 3 * v * v * t * x1 + 3 * v * t * t * x2 + t * t * t;
	};

	var curveY = function(t){
		var v = 1 - t;
		return 3 * v * v * t * y1 + 3 * v * t * t * y2 + t * t * t;
	};

	var derivativeCurveX = function(t){
		var v = 1 - t;
		return 3 * (2 * (t - 1) * t + v * v) * x1 + 3 * (- t * t * t + 2 * v * t) * x2;
	};

	return function(t){

		var x = t, t0, t1, t2, x2, d2, i;

		// First try a few iterations of Newton's method -- normally very fast.
		for (t2 = x, i = 0; i < 8; i++){
			x2 = curveX(t2) - x;
			if (Math.abs(x2) < epsilon) return curveY(t2);
			d2 = derivativeCurveX(t2);
			if (Math.abs(d2) < 1e-6) break;
			t2 = t2 - x2 / d2;
		}

		t0 = 0, t1 = 1, t2 = x;

		if (t2 < t0) return curveY(t0);
		if (t2 > t1) return curveY(t1);

		// Fallback to the bisection method for reliability.
		while (t0 < t1){
			x2 = curveX(t2);
			if (Math.abs(x2 - x) < epsilon) return curveY(t2);
			if (x > x2) t0 = t2;
			else t1 = t2;
			t2 = (t1 - t0) * .5 + t0;
		}

		// Failure
		return curveY(t2);

	};
};
var duration = 200;
var epsilon = (1000 / 60 / duration) / 4;
var timingFunction = bezier(0.08, 1.05, 0.95, 0.12, epsilon);

paths = [];
paths[0] = Snap('#cd-changing-path-1');
paths[1] = Snap('#cd-changing-path-2');
paths[2] = Snap('#cd-changing-path-3');

pathSteps = [];
for (var n = 0; n < 6; n++) {
	pathSteps[n] = $('.cd-svg-bg').data('step'+(n+1));
};

function animateModal(paths, pathSteps, duration, animationType) {
	var path1 = ( animationType == 'open' ) ? pathSteps[1] : pathSteps[0],
		path2 = ( animationType == 'open' ) ? pathSteps[3] : pathSteps[2],
		path3 = ( animationType == 'open' ) ? pathSteps[5] : pathSteps[4];
	
	paths[0].animate({'d': path1}, duration, timingFunction);
	paths[1].animate({'d': path2}, duration, timingFunction);
	paths[2].animate({'d': path3}, duration, timingFunction);
}

modalTrigger =  $('a[data-type="cd-modal-trigger"]');
modal = $('.cd-modal'), coverLayer = $('.cd-cover-layer');

$(document).on('click', 'a[data-type="cd-modal-trigger"]', function(eventObject){
	modal = $(this).siblings('.cd-modal');
	coverLayer = $(this).siblings('.cd-cover-layer');
	$([modal.get(0), coverLayer.get(0)]).addClass('modal-is-visible');
	animateModal(paths, pathSteps, duration, 'open');

	modal.focus();
});
 
modal.on('click', '.modal-close', function(event){
	event.preventDefault();
	modal.removeClass('modal-is-visible');
	coverLayer.removeClass('modal-is-visible');
	animateModal(paths, pathSteps, duration, 'close');
});
