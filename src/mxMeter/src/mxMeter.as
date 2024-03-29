﻿package 
{
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormatAlign;
	import lesta.api.GameAPI;
	import lesta.api.ModBase;
	import flash.text.TextField;
	import flash.text.TextFormat;

	public class mxMeter extends ModBase 
	{
		private static const SHOW_PUK_INDICATOR:String = "mxMeter.showPukIndicator";
		private static const UPDATE_PUK_INDICATOR:String = "mxMeter.updatePukIndicator";
		private static const HIDE_PUK_INDICATOR:String = "mxMeter.hidePukIndicator";
		private var _puk_indicator:TextField;

		public function mxMeter() 
		{
			super();
			this._puk_indicator = null;
		}
		
		override public function init():void 
		{
			super.init();
			gameAPI.data.addCallBack(SHOW_PUK_INDICATOR, this.onShowPukIndicator);
			gameAPI.data.addCallBack(UPDATE_PUK_INDICATOR, this.onUpdatePukIndicator);
			gameAPI.data.addCallBack(HIDE_PUK_INDICATOR, this.onHidePukIndicator);
		}
		
		override public function fini():void 
		{
			gameAPI.data.removeCallBack();
			super.fini();
		}

		private function onShowPukIndicator(x:int, y:int, font_size:int, font_color:int, width:int, label:String):void
		{
			if (this._puk_indicator) {
				gameAPI.stage.removeChild(this._puk_indicator);
				this._puk_indicator = null;
			}
			this._puk_indicator = new TextField;
			this._puk_indicator.autoSize = TextFieldAutoSize.LEFT;
			this._puk_indicator.defaultTextFormat = new TextFormat("$WWSDefaultFont", font_size, font_color);
			//this._puk_indicator.defaultTextFormat.align = TextFormatAlign.RIGHT
			this._puk_indicator.text = label;
			this._puk_indicator.width = width;
			//this._puk_indicator.border = true;
			//this._puk_indicator.borderColor = 0xff0000;
			if (x >= 0) {
				this._puk_indicator.x = x
			} else {
				this._puk_indicator.x = gameAPI.stage.width + x;
			}
			if (y >= 0) {
				this._puk_indicator.y = y;
			} else {
				this._puk_indicator.y = gameAPI.stage.height + y
			}
			gameAPI.stage.addChild(this._puk_indicator);
		}

		private function onUpdatePukIndicator(label:String):void
		{
			if (this._puk_indicator) {
				this._puk_indicator.text = label;
			}
		}

		private function onHidePukIndicator():void
		{
			if (this._puk_indicator) {
				gameAPI.stage.removeChild(this._puk_indicator);
				this._puk_indicator = null;
			}
		}
	}
}