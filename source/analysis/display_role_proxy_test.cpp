#include "../display_role_proxy.h"

#include <QtGui/QStandardItemModel>

namespace {
bool g_enabled = true;
bool enabled() { return g_enabled; }
QString lookup(const QString &source) {
    return source == QStringLiteral("File") ? QStringLiteral("文件") : QString();
}
}

int main() {
    QStandardItemModel source(1, 1);
    const QModelIndex original = source.index(0, 0);
    if (!source.setData(original, QStringLiteral("File"), Qt::DisplayRole) ||
        !source.setData(original, QStringLiteral("unmodified"), Qt::UserRole))
        return 1;

    MariDisplayRoleProxyModel proxy(lookup, enabled, nullptr);
    proxy.setSourceModel(&source);
    const QModelIndex display = proxy.index(0, 0);
    if (proxy.data(display, Qt::DisplayRole).toString() != QStringLiteral("文件") ||
        proxy.data(display, Qt::UserRole).toString() != QStringLiteral("unmodified") ||
        source.data(original, Qt::DisplayRole).toString() != QStringLiteral("File"))
        return 2;

    if (proxy.setData(display, QStringLiteral("中文"), Qt::DisplayRole) ||
        proxy.setItemData(display, {{Qt::DisplayRole, QStringLiteral("中文")}}) ||
        proxy.setHeaderData(0, Qt::Horizontal, QStringLiteral("中文")))
        return 3;
    if (source.data(original, Qt::DisplayRole).toString() != QStringLiteral("File"))
        return 4;

    g_enabled = false;
    return proxy.data(display, Qt::DisplayRole).toString() == QStringLiteral("File")
        ? 0 : 5;
}
