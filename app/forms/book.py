
from wtforms import Form, StringField, IntegerField,FileField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30), DataRequired()])
    page = IntegerField(validators=[NumberRange(min=1, max=30)], default=1)


class DriftForm(Form):
    recipient_name = StringField('收件人姓名', validators=[DataRequired(), Length(min=2, max=20)])
    mobile = StringField('手机号', validators=[DataRequired(), Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField('留言')
    address = StringField('地址', validators=[DataRequired(), Length(min=10, max=70, message='地址必须大于10个字符')])

class LengForm(Form):
    title=StringField(validators=[Length(min=1, max=30), DataRequired(message='书名不能为空')])
    isbn = StringField(validators=[Length(min=13, max=13), DataRequired(message='书号不能为空')])
    author=StringField('作者')
    publisher=StringField('出版社')
    summary=StringField('简介')
    image=StringField("上传图片")
