#pragma once

#include <QtCore/QIdentityProxyModel>
#include <QtCore/QString>
#include <QtCore/QVariant>

// The delegate reads Chinese DisplayRole text through this private paint proxy.
// The source model retains its original data, and paint-time callers cannot
// write translated values back through the proxy.
class MariDisplayRoleProxyModel final : public QIdentityProxyModel {
public:
    using Lookup = QString (*)(const QString &);
    using Enabled = bool (*)();

    MariDisplayRoleProxyModel(Lookup lookup, Enabled enabled, QObject *parent)
        : QIdentityProxyModel(parent), lookup_(lookup), enabled_(enabled) {}

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override {
        const QVariant source = QIdentityProxyModel::data(index, role);
        if (role != Qt::DisplayRole || !enabled_())
            return source;
        const QString display = lookup_(source.toString());
        return display.isEmpty() ? source : QVariant(display);
    }

    bool setData(const QModelIndex &, const QVariant &, int = Qt::EditRole) override {
        return false;
    }

    bool setItemData(const QModelIndex &, const QMap<int, QVariant> &) override {
        return false;
    }

    bool setHeaderData(int, Qt::Orientation, const QVariant &,
                       int = Qt::EditRole) override {
        return false;
    }

private:
    Lookup lookup_;
    Enabled enabled_;
};
