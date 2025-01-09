package
{
   import lesta.unbound.expression.ExpressionsDict;

   public class USSExpressions
   {
      public function USSExpressions()
      {
         super();
      }
   
      public static function doInitializeStatic(param1:ExpressionsDict, param2:ExpressionsDict) : void
      {
         var expr:String = null;

         expr = "\'lesta.api.UbModController\'";
         param1[expr] = expr01;
         param2[expr] = null;

         expr = "\'ub_print\'";
         param1[expr] = expr02;
         param2[expr] = null;

         expr = " mx_print";
         param1[expr] = expr03;
         param2[expr] = new <String>["mx_print"];

         expr = "\'ub_visible\'";
         param1[expr] = expr04;
         param2[expr] = null;

         expr = " mx_visible";
         param1[expr] = expr05;
         param2[expr] = new <String>["mx_visible"];

         expr = "ub_visible";
         param1[expr] = expr06;
         param2[expr] = new <String>["ub_visible"];

         expr = "\'MxMeter_stageEntity\'";
         param1[expr] = expr07;
         param2[expr] = null;

         expr = " CC.stage";
         param1[expr] = expr08;
         param2[expr] = new <String>["CC"];

         expr = "\'MxMeter_stage\'";
         param1[expr] = expr09;
         param2[expr] = null;

         expr = " [\'MxMeter_stageEntity.stage.evStageSizeChanged\']";
         param1[expr] = expr10;
         param2[expr] = null;

         expr = " MxMeter_stageEntity.stage";
         param1[expr] = expr11;
         param2[expr] = new <String>["MxMeter_stageEntity"];

         expr = "MxMeter_stage.width - 174";
         param1[expr] = expr12;
         param2[expr] = new <String>["MxMeter_stage"];

         expr = "5px";
         param1[expr] = expr13;
         param2[expr] = null;

         expr = "80px";
         param1[expr] = expr14;
         param2[expr] = null;

         expr = "ub_print";
         param1[expr] = expr15;
         param2[expr] = new <String>["ub_print"];
      }

      public static function expr01(param1:Object) : *
      {
         return "lesta.api.UbModController";
      }

      public static function expr02(param1:Object) : *
      {
         return "ub_print";
      }

      public static function expr03(param1:Object) : *
      {
         return param1.mx_print;
      }

      public static function expr04(param1:Object) : *
      {
         return "ub_visible";
      }

      public static function expr05(param1:Object) : *
      {
         return param1.mx_visible;
      }

      public static function expr06(param1:Object) : *
      {
         return param1.ub_visible;
      }

      public static function expr07(param1:Object) : *
      {
         return "MxMeter_stageEntity";
      }

      public static function expr08(param1:Object) : *
      {
         return param1.getPropertySecure("CC","stage");
      }

      public static function expr09(param1:Object) : *
      {
         return "MxMeter_stage";
      }

      public static function expr10(param1:Object) : *
      {
         return ["MxMeter_stageEntity.stage.evStageSizeChanged"];
      }

      public static function expr11(param1:Object) : *
      {
         return param1.getPropertySecure("MxMeter_stageEntity","stage");
      }

      public static function expr12(param1:Object) : *
      {
         return param1.getPropertySecure("MxMeter_stage","width") - 174;
      }

      public static function expr13(param1:Object) : *
      {
         return 5;
      }

      public static function expr14(param1:Object) : *
      {
         return 80;
      }

      public static function expr15(param1:Object) : *
      {
         return param1.ub_print;
      }
   }
}
