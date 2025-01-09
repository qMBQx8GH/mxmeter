package
{
   import flash.display.Sprite;
   import lesta.unbound.expression.ExpressionsDict;

   public class mxMeter extends Sprite
   {
      public function mxMeter()
      {
         super();
      }

      public function doInitialize(param1:ExpressionsDict, param2:ExpressionsDict) : void
      {
         USSExpressions.doInitializeStatic(param1,param2);
      }
   }
}
