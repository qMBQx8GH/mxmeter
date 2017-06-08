package 
{
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

		private function onShowPukIndicator(label:String):void
		{
			this._puk_indicator = new TextField;
			this._puk_indicator.defaultTextFormat = new TextFormat("$WWSDefaultFont", 18, 0xfefefe);
			this._puk_indicator.text = label;
			this._puk_indicator.width = 165;
			this._puk_indicator.x = gameAPI.stage.width - this._puk_indicator.width;
			this._puk_indicator.y = 0;
			gameAPI.stage.addChild(this._puk_indicator);
		}

		private function onUpdatePukIndicator(label:String):void
		{
			this._puk_indicator.text = label;
		}

		private function onHidePukIndicator():void
		{
			if (this._puk_indicator)
			{
				gameAPI.stage.removeChild(this._puk_indicator);
				this._puk_indicator = null;
			}
		}
	}
}