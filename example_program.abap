*&---------------------------------------------------------------------*
*& Report ZEXAMPLE_CLOUD_ISSUES
*&---------------------------------------------------------------------*
REPORT zexample_cloud_issues.

* This program demonstrates common Open SQL syntax issues
* that cause "Syntax error in restricted language scope" errors
* when running ATC checks with ABAP_CLOUD_READINESS variant

TABLES: mara, marc, mard.

DATA: ls_mara TYPE mara,
      lt_marc TYPE TABLE OF marc,
      lv_count TYPE i.

START-OF-SELECTION.

  * Issue 1: Basic SELECT statement not allowed in restricted language
  SELECT matnr mtart matkl FROM mara 
    INTO ls_mara 
    WHERE matnr = '000000000000000001'.

  * Issue 2: SELECT with APPENDING not allowed
  SELECT matnr werks FROM marc 
    APPENDING TABLE lt_marc 
    WHERE matnr = '000000000000000001'.

  * Issue 3: INSERT statement not allowed
  INSERT INTO mara VALUES ls_mara.

  * Issue 4: UPDATE statement not allowed
  UPDATE mara SET mtart = 'FERT' WHERE matnr = '000000000000000001'.

  * Issue 5: DELETE statement not allowed
  DELETE FROM mara WHERE matnr = '000000000000000001'.

  * Issue 6: System field access not allowed
  SY-SUBRC = 0.
  SY-DBCNT = 1.
  SY-TABIX = 0.

  * Issue 7: COMMIT WORK without AND WAIT
  COMMIT WORK.

  * Issue 8: ROLLBACK WORK without AND WAIT
  ROLLBACK WORK.

  * Issue 9: Function module call with destination
  CALL FUNCTION 'BAPI_MATERIAL_GET_DETAIL'
    DESTINATION 'SYS'
    EXPORTING
      material = '000000000000000001'
    IMPORTING
      material_data = ls_mara.

  * Issue 10: Function module call with exceptions
  CALL FUNCTION 'BAPI_MATERIAL_SAVE'
    EXPORTING
      material_data = ls_mara
    EXCEPTIONS
      error = 1.

  * Issue 11: System field assignment
  lv_count = SY-DBCNT.

  * Issue 12: Complex SELECT with multiple clauses
  SELECT matnr mtart matkl 
    FROM mara 
    INTO TABLE @DATA(lt_mara)
    WHERE matnr IN @lt_marc
    ORDER BY matnr
    GROUP BY mtart.

END-OF-SELECTION.