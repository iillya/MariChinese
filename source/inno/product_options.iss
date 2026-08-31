{ Included after the common state helpers. }
var
  DpiPage: TInputQueryWizardPage;
  DpiEnabled: TNewCheckBox;
  DpiLoadedDirectory: String;

procedure CreateProductOptions;
begin
  DpiPage := CreateInputQueryPage(wpSelectTasks, '显示设置', '配置高 DPI 视口修正',
    '普通屏幕可保持关闭。此设置仅影响 Mari 视口显示，不修改工程数据。');
  DpiPage.Add('缩放系数（1.0～3.0）：', False);
  DpiPage.Values[0] := '1.75';
  DpiEnabled := TNewCheckBox.Create(WizardForm);
  DpiEnabled.Parent := DpiPage.Surface;
  DpiEnabled.Caption := '启用高 DPI 视口修正';
  DpiEnabled.Checked := False;
  DpiEnabled.SetBounds(0, DpiPage.Edits[0].Top + DpiPage.Edits[0].Height + ScaleY(20),
    DpiPage.SurfaceWidth, ScaleY(24));
end;

procedure CurPageChanged(CurPageID: Integer);
var
  FileName, Directory: String;
begin
  if CurPageID <> DpiPage.ID then Exit;
  Directory := WizardDirValue;
  if DpiLoadedDirectory = Directory then Exit;
  FileName := AddBackslash(Directory) + 'ChineseLauncher\settings.ini';
  DpiEnabled.Checked := StrToIntDef(GetIniString('Dpi', 'Enabled', '0', FileName), 0) <> 0;
  DpiPage.Values[0] := GetIniString('Dpi', 'ScaleFactor', '1.75', FileName);
  DpiLoadedDirectory := Directory;
end;

function ValidScale(Value: String): Boolean;
var
  I, Fraction, Whole, Digits, Dot: Integer;
begin
  Result := False;
  if (Length(Value) < 1) or (Length(Value) > 4) then Exit;
  Dot := Pos('.', Value);
  if Dot = 0 then begin
    Whole := StrToIntDef(Value, -1);
    Result := (Whole >= 1) and (Whole <= 3);
    Exit;
  end;
  if (Dot <> 2) or (Length(Value) <= Dot) then Exit;
  for I := 1 to Length(Value) do
    if (I <> Dot) and ((Value[I] < '0') or (Value[I] > '9')) then Exit;
  Whole := StrToIntDef(Copy(Value, 1, 1), -1);
  Digits := Length(Value) - Dot;
  Fraction := StrToIntDef(Copy(Value, Dot + 1, Digits), -1);
  Result := (Whole >= 1) and (Whole <= 3) and (Fraction >= 0) and
    ((Whole < 3) or (Fraction = 0));
end;

procedure ApplyProductOptions;
var
  FileName, Scale, Enabled: String;
begin
  FileName := InstallRoot + '\settings.ini';
  if DpiLoadedDirectory = '' then begin
    DpiEnabled.Checked := StrToIntDef(GetIniString('Dpi', 'Enabled', '0', FileName), 0) <> 0;
    DpiPage.Values[0] := GetIniString('Dpi', 'ScaleFactor', '1.75', FileName);
  end;
  Enabled := '0';
  if DpiEnabled.Checked then Enabled := '1';
  Enabled := ExpandConstant('{param:DPI|' + Enabled + '}');
  Scale := ExpandConstant('{param:DPISCALE|' + DpiPage.Values[0] + '}');
  if ((Enabled <> '0') and (Enabled <> '1')) or not ValidScale(Scale) then
    RaiseException('高 DPI 设置无效。缩放系数须为 1.0～3.0。');
  if not SetIniString('Dpi', 'Enabled', Enabled, FileName) or
    not SetIniString('Dpi', 'ScaleFactor', Scale, FileName) then
    RaiseException('无法保存高 DPI 设置。请检查目录权限后重试。');
end;
